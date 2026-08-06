<?php
session_start();
require_once 'config.php';

// path 없는데 404 발생 안하는 문제
if (isset($_SERVER['PATH_INFO']) && $_SERVER['PATH_INFO'] !== '/') {
    http_response_code(404);
    echo "Not Found";
    exit;
}

// 로그인 체크
if (!isset($_SESSION['user'])) {
    die("Login required");
}

$uploadDir = __DIR__ . '/uploads/';
if (!is_dir($uploadDir)) {
    mkdir($uploadDir, 0777, true); }

$uploadUrl = null;

if ($_SERVER['REQUEST_METHOD'] === 'POST') {

    $title   = $_POST['title'];    // 필터링 없음 → Stored XSS 가능
    $content = $_POST['content'];  // 필터링 없음 → Stored XSS 가능
    $uid     = $_SESSION['user'];

    // SQL 인젝션 취약점
    $sql = "INSERT INTO posts (title, content, author_id) VALUES ('$title', '$content', $uid)";
    $pdo->exec($sql);

    $postId = $pdo->lastInsertId();

    $uploadUrl = null;

    if (isset($_FILES['file']) && $_FILES['file']['error'] === UPLOAD_ERR_OK) {
        $file = $_FILES['file'];

        $filename = $file['name'];

        $targetPath = $uploadDir . $filename;

        if (move_uploaded_file($file['tmp_name'], $targetPath)) {
            $uploadUrl = 'uploads/' . $filename;
            $sql2 = "UPDATE posts SET file_path = '$uploadUrl' WHERE id = $postId";
            $pdo->exec($sql2);
        }
    }

    header("Location: /posts.php");
    exit;
}
?>
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Create Post with File</title>
</head>
<body>
<h1>새 글 작성 + 파일 업로드</h1>

<p>Logged in as: <?= $_SESSION['username'] ?></p>
<p><a href="posts.php">[게시판 목록]</a></p>

<form method="POST" enctype="multipart/form-data">
    <p>
        <label>Title</label><br>
        <input type="text" name="title" placeholder="title">
    </p>
    <p>
        <label>Content</label><br>
        <textarea name="content" placeholder="content"></textarea>
    </p>
    <p>
        <label>File upload</label><br>
        <input type="file" name="file">
    </p>
    <button type="submit">작성</button>
</form>


</body>
</html>

