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

resource "aws_eks_node_group" "this" {
  cluster_name    = aws_eks_cluster.this.name
  node_group_name = "${var.cluster_name}-nodes"
  node_role_arn   = local.lab_role_arn
  subnet_ids      = var.subnet_ids
  instance_types  = [var.node_instance_type]

  scaling_config {
    desired_size = var.node_desired_size
    min_size     = var.node_min_size
    max_size     = var.node_max_size
  }
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
