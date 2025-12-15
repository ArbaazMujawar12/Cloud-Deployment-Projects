#!/bin/bash
sudo yum update -y
sudo yum install -y httpd
sudo systemctl start httpd
sudo systemctl enable httpd

cat <<EOF > /var/www/html/index.html
<!DOCTYPE html>
<html>
<head>
<title>Smart Product Store</title>
<style>
body { margin:0; font-family: Arial, Helvetica, sans-serif; background:#f4f6f8; }
header { background:#0f172a; padding:15px; }
nav a { color:white; margin:15px; text-decoration:none; font-weight:bold; }
nav a:hover { color:#38bdf8; }
.container { padding:60px; text-align:center; }
.card { background:white; padding:40px; border-radius:10px; box-shadow:0 4px 12px rgba(0,0,0,0.1); display:inline-block; }
footer { background:#0f172a; color:white; text-align:center; padding:10px; position:fixed; bottom:0; width:100%; }
.button { display:inline-block; margin:10px; padding:12px 25px; background:#2563eb; color:white; text-decoration:none; border-radius:6px; }
.button:hover { background:#1e40af; }
</style>
</head>
<body>
<header>
<nav>
<a href="/home">Home</a>
<a href="/mobile/">Mobile</a>
<a href="/laptop/">Laptop</a>
<a href="/accessories/">Accessories</a>
</nav>
</header>


<div class="container">
<div class="card">
<h1>Welcome to Smart Product Store</h1>
<p>Served from: <b>$(hostname -f)</b></p>
<p>Select a category from the menu</p>
</div>
</div>


<footer>
<p>AWS ALB Project</p>
</footer>
</body>
</html>
EOF