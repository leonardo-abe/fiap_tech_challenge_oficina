# Banco de dados, aplicado via kubectl (igual à criação do cluster em main.tf) em vez
# do provider "kubernetes" do Terraform - esse provider só consegue se conectar depois
# que o cluster existe, o que obrigava a rodar "terraform apply" duas vezes (uma só
# para o cluster, outra para o resto). Usando kubectl via local-exec, tudo roda em
# sequência dentro da MESMA apply, sem essa limitação.
resource "null_resource" "postgres" {
  # precisa do add-on EBS CSI (ver main.tf) já instalado - senão o PVC do Postgres fica
  # "Pending" para sempre e o rollout abaixo nunca completa.
  depends_on = [null_resource.kubeconfig, aws_eks_addon.ebs_csi]

  triggers = {
    postgres_user = var.postgres_user
    postgres_db   = var.postgres_db
    manifest_hash = filesha256("${path.module}/postgres.yaml")
  }

  # um provisioner por comando (em vez de um heredoc multi-linha) de propósito - o
  # local-exec no Windows roda via "cmd /C", que não lida bem com múltiplas linhas
  # num único comando (mesmo problema de portabilidade já visto com caminhos "./" em
  # main.tf). Cada provisioner abaixo é uma única linha, portável em qualquer SO.
  provisioner "local-exec" {
    command = "kubectl --kubeconfig ${var.kubeconfig_path} create namespace oficina --dry-run=client -o yaml | kubectl --kubeconfig ${var.kubeconfig_path} apply -f -"
  }

  provisioner "local-exec" {
    command = "kubectl --kubeconfig ${var.kubeconfig_path} create secret generic postgres-credentials -n oficina --from-literal=POSTGRES_USER=${var.postgres_user} --from-literal=POSTGRES_PASSWORD=${var.postgres_password} --from-literal=POSTGRES_DB=${var.postgres_db} --dry-run=client -o yaml | kubectl --kubeconfig ${var.kubeconfig_path} apply -f -"
  }

  provisioner "local-exec" {
    command = "kubectl --kubeconfig ${var.kubeconfig_path} apply -f postgres.yaml"
  }

  provisioner "local-exec" {
    command = "kubectl --kubeconfig ${var.kubeconfig_path} rollout status deployment/postgres -n oficina --timeout=240s"
  }
}
