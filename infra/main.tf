# Cria o cluster Kubernetes local (kind) via CLI em vez de um provider Terraform
# dedicado: providers de terceiros para kind tendem a ser instáveis entre versões do
# kind/terraform, enquanto a CLI oficial funciona de forma previsível em qualquer
# máquina que já tenha Docker instalado.
resource "null_resource" "kind_cluster" {
  triggers = {
    cluster_name = var.cluster_name
    config_hash  = filesha256("${path.module}/kind-config.yaml")
  }

  provisioner "local-exec" {
    # caminhos relativos simples (sem "./" ou path.module) - no Windows, o cmd.exe que
    # executa o local-exec interpreta mal um prefixo "./" combinado com certos
    # separadores, e falha com "sintaxe do nome do arquivo incorreta".
    command = "kind create cluster --name ${self.triggers.cluster_name} --config kind-config.yaml --kubeconfig ${var.kubeconfig_path} --wait 120s"
  }

  provisioner "local-exec" {
    when    = destroy
    command = "kind delete cluster --name ${self.triggers.cluster_name}"
  }
}
