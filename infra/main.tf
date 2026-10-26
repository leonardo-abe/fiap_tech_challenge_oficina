data "aws_caller_identity" "current" {}

locals {
  # "LabRole" é o role pré-criado pelo AWS Academy Learner Lab, já com as policies
  # necessárias para o EKS (AmazonEKSClusterPolicy/AmazonEKSWorkerNodePolicy) anexadas -
  # o Academy não permite criar roles IAM novos, então reaproveitamos este em vez de um
  # "aws_iam_role" próprio (que falharia por falta de permissão de qualquer forma).
  lab_role_arn = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/LabRole"
}

resource "aws_eks_cluster" "this" {
  name     = var.cluster_name
  role_arn = local.lab_role_arn
  version  = "1.31"

  vpc_config {
    subnet_ids = var.subnet_ids
  }
}

resource "aws_launch_template" "nodes" {
  name_prefix = "${var.cluster_name}-nodes-"

  metadata_options {
    http_endpoint               = "enabled"
    http_tokens                 = "required"
    http_put_response_hop_limit = 2
  }
}

resource "aws_eks_node_group" "this" {
  cluster_name    = aws_eks_cluster.this.name
  node_group_name = "${var.cluster_name}-nodes"
  node_role_arn   = local.lab_role_arn
  subnet_ids      = var.subnet_ids
  instance_types  = [var.node_instance_type]

  launch_template {
    id      = aws_launch_template.nodes.id
    version = aws_launch_template.nodes.latest_version
  }

  scaling_config {
    desired_size = var.node_desired_size
    min_size     = var.node_min_size
    max_size     = var.node_max_size
  }
}

# obrigatório para o PersistentVolumeClaim do Postgres sair de "Pending": o
# provisionador de volume "in-tree" (kubernetes.io/aws-ebs, que a StorageClass "gp2"
# padrão do EKS ainda referencia) está depreciado e não provisiona mais nada em
# clusters recentes - sem este add-on, o PVC fica pendurado indefinidamente e o pod do
# Postgres nunca chega a ser agendado ("unbound immediate PersistentVolumeClaims"). O
# node role (LabRole) já tem as permissões de EC2/EBS necessárias (política ampla do
# AWS Academy), então não precisamos de uma role IRSA dedicada para o add-on.
resource "aws_eks_addon" "ebs_csi" {
  cluster_name                = aws_eks_cluster.this.name
  addon_name                  = "aws-ebs-csi-driver"
  resolve_conflicts_on_create = "OVERWRITE"
  resolve_conflicts_on_update = "OVERWRITE"

  depends_on = [aws_eks_node_group.this]
}

# gera o kubeconfig (via CLI "aws eks update-kubeconfig", a mesma forma documentada pela
# própria AWS) só depois que cluster E node group estão prontos - os passos seguintes
# (Postgres, aplicação) precisam de nós de verdade para agendar pods.
resource "null_resource" "kubeconfig" {
  depends_on = [aws_eks_node_group.this]

  triggers = {
    cluster_name = var.cluster_name
  }

  provisioner "local-exec" {
    command = "aws eks update-kubeconfig --name ${var.cluster_name} --region ${var.aws_region} --kubeconfig ${var.kubeconfig_path}"
  }
}
