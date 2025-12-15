#!/bin/bash
sudo yum update -y
sudo yum install -y httpd
sudo systemctl start httpd
sudo systemctl enable httpd

sudo mkdir -p /var/www/html/mobile

cat <<EOF > /var/www/html/mobile/index.html
<!DOCTYPE html>
<html>
<head>
<title>Mobile Store</title>

<style>
body {
    margin: 0;
    font-family: Arial, Helvetica, sans-serif;
    background-color: #f4f6f8;
}

header {
    background-color: #0f172a;
    padding: 15px;
}

nav a {
    color: white;
    margin: 15px;
    text-decoration: none;
    font-weight: bold;
}

nav a:hover {
    color: #38bdf8;
}

.container {
    padding: 60px;
    text-align: center;
}

.card {
    background: white;
    padding: 40px;
    border-radius: 10px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    display: inline-block;
}

footer {
    background-color: #0f172a;
    color: white;
    text-align: center;
    padding: 10px;
    position: fixed;
    bottom: 0;
    width: 100%;
}
</style>

</head>
<body>

<header>
<nav>
<a href="/">Home</a>
<a href="/mobile/">Mobile</a>
<a href="/laptop/">Laptop</a>
<a href="/accessories/">Accessories</a>
</nav>
</header>

<div class="container">
<div class="card">
<h1>📱 Mobile Store</h1>
<p>Latest smartphones available</p>
<p><b>Server:</b> $(hostname -f)</p>
</div>
</div>

<footer>
<p>AWS ALB Project</p>
</footer>

</body>
</html>
EOF
