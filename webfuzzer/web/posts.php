<?php
if (isset($_SERVER['PATH_INFO']) && $_SERVER['PATH_INFO'] !== '') {
    http_response_code(404);
    echo "Not Found";
    exit;
}

session_start();
require_once "config.php";

// -------------------------------
// DELETE POST
// -------------------------------
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['delete_id'])) {

    if (!isset($_SESSION['user'])) {
        die("Login required");
    }

    $delete_id = $_POST['delete_id'];

    $sql = "SELECT author_id FROM posts WHERE id = $delete_id";
    $post = $pdo->query($sql)->fetch(PDO::FETCH_ASSOC);

    if (!$post) {
        die("Post not found");
    }

    $current_user = $_SESSION['user'];
    $role = $_SESSION['role'] ?? 'user';

    if ($role === 'admin' || $post['author_id'] == $current_user) {
        $pdo->exec("DELETE FROM posts WHERE id = $delete_id"); // SQLi 가능
    } else {
        die("Not allowed");
    }

    header("Location: /posts.php");
    exit;
}

// 목록 조회
$res = $pdo->query("SELECT posts.*, users.username FROM posts JOIN users ON posts.author_id = users.id ORDER BY posts.id DESC");
$posts = $res->fetchAll(PDO::FETCH_ASSOC);
?>
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Posts</title>
</head>
<body>
<h1>Posts</h1>

<p>Logged in as: <?= $_SESSION['username'] ?></p>

<p>
    <!-- 새 글 + 파일 업로드 페이지로 이동 -->
    <a href="create_post.php">[글 작성 / 파일 업로드]</a>
</p>

<hr>
<ul>
<?php foreach ($posts as $p): ?>
    <li>
        <a href="post.php?id=<?= $p['id'] ?>"><?= $p['title'] ?></a>
        by <?= $p['username'] ?>
    </li>
<?php endforeach; ?>
</ul>



</body>
</html>
