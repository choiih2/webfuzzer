<?php
if (isset($_SERVER['PATH_INFO']) && $_SERVER['PATH_INFO'] !== '') {
    http_response_code(404);
    echo "Not Found";
    exit;
}
require_once 'config.php';
session_start();

if (!isset($_SESSION['user'])) {
    die("Login required");
}

if (!isset($_GET['id'])) {
    die("No id");
}
$id = $_GET['id']; // 필터 없음 →  취약점 발생
$sql = "SELECT posts.*, users.username FROM posts JOIN users ON posts.author_id = users.id WHERE posts.id = $id";
$post = $pdo->query($sql)->fetch(PDO::FETCH_ASSOC);

if (!$post) {
    die("Post not found");
}
?>
<!DOCTYPE html>
<html>
<head>
   <meta charset="utf-8">
   <title><?=$post['title']?></title>
</head>
<body>
<h1><?= $post['title'] ?></h1>

<p>by <?= $post['username'] ?></p>

<hr>

<div>
    <?= $post['content'] ?>
</div>


<?php if (!empty($post['file_path'])): ?>
    <p>첨부 파일: <a href="<?= $post['file_path'] ?>"><?= $post['file_path'] ?></a></p>
<?php endif; ?>

<p><a href="posts.php">목록으로</a></p>

</body>
</html>

