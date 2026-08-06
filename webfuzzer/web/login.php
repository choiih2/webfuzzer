<?php
if (isset($_SERVER['PATH_INFO']) && $_SERVER['PATH_INFO'] !== '') {
    http_response_code(404);
    echo "Not Found";
    exit;
}
session_start();
require_once "config.php";

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $email = $_POST['email'] ?? '';
    $password = $_POST['password'] ?? '';

// 취약점 존재
    $sql = "SELECT * FROM users WHERE email='$email' AND password='$password'";
    $res = $pdo->query($sql)->fetch(PDO::FETCH_ASSOC);

    if ($res) {
        $_SESSION['user'] = $res['id'];
        $_SESSION['username'] = $res['username'];
        header("Location: /posts.php");
        exit;
    } else {
        echo "<p style='color:red'>Login failed</p>";
    }
}
?>

<h1>Login</h1>
<form method="POST">
  <input name="email" placeholder="email"><br>
  <input name="password" placeholder="password"><br>
  <button type="submit">Login</button>
</form>

