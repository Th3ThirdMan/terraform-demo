provider "aws" {
  region = "eu-west-1"
}

data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }
}

resource "aws_security_group" "web" {
  name = "flask-sg"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port = 5000
    to_port = 5000
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "web" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t3.micro"
  key_name ="terraform-key"

  associate_public_ip_address = true
  vpc_security_group_ids      = [aws_security_group.web.id]

  user_data = <<-EOF
#!/bin/bash
apt-get update -y
apt-get install -y docker.io git
systemctl start docker
systemctl enable docker

cd /home/ubuntu
git clone https://github.com/Th3ThirdMan/flask-terraform-demo.git
cd flask-terraform-demo/app

docker build -t flask-app .
docker run -d -p 5000:5000 flask-app
EOF

  tags = {
    Name = "flask-demo"
  }
}

output "public_ip" {
  value = aws_instance.web.public_ip
}