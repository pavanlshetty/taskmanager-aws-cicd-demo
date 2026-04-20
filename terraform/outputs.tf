output "ec2_public_ip" {
  description = "Public IP of the EC2 instance"
  value       = aws_instance.app_server.public_ip
}

output "application_url" {
  description = "URL to access the Task Manager application"
  value       = "http://${aws_instance.app_server.public_ip}:5000"
}

output "ssh_connection" {
  description = "SSH command to connect to EC2 instance"
  value       = "ssh -i ~/.ssh/taskmanager-app-key ubuntu@${aws_instance.app_server.public_ip}"
}