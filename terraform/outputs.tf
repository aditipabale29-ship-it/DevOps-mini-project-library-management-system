output "security_group_id" {
  description = "ID of the Library Management security group"
  value       = aws_security_group.library_sg.id
}

output "aws_region" {
  description = "AWS region used by the project"
  value       = var.aws_region
}
