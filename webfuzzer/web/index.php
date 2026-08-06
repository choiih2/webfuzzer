<?php
if (isset($_SERVER['PATH_INFO']) && $_SERVER['PATH_INFO'] !== '') {
    http_response_code(404);
    echo "Not Found";
    exit;
}// index.php
?>
<!doctype html>
<html>
<head>
    <meta charset="utf-8">
    <title>Home</title>
</head>
<body>
<h1>VulnApp</h1>
<p>
    <a href="login.php">login</a>,
    <a href="posts.php">posts</a>
</p>
</body>
</html>

