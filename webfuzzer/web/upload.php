<?php
if (isset($_SERVER['PATH_INFO']) && $_SERVER['PATH_INFO'] !== '/') {
    http_response_code(404);
    echo "Not Found";
    exit;
}

session_start();
require_once 'config.php';

if (!isset($_SESSION['user'])) {
    die("Login required");
}

$uploadDir = __DIR__ . '/uploads/';

if (!is_dir($uploadDir)) {
    mkdir($uploadDir, 0777, true);
}

// 파일 업로드 처리
if ($_SERVER['REQUEST_METHOD'] === 'POST') {

    // 취약점 1: 파일이 정말 업로드 되었는지 최소한의 체크만 수행
    if (!isset($_FILES['file']) || $_FILES['file']['error'] !== UPLOAD_ERR_OK) {
        die("Upload failed");
    }

    $file = $_FILES['file'];

    // 취약점 2: 원본 파일 이름 그대로 사용 (경로 정규화 미흡)
    $filename = $file['name'];

    // 취약점 3: 확장자 / MIME 타입 검증 전혀 없음
    // 예: .php, .phtml, .php5 등도 그대로 허용

    // 취약점 4: 파일 내용을 검사하지 않음 (이미지 위장 악성코드 가능)

    $targetPath = $uploadDir . $filename;

    if (move_uploaded_file($file['tmp_name'], $targetPath)) {
        $urlPath = 'uploads/' . $filename;
        echo "<p>Upload success!</p>";
        echo "<p>File URL: <a href=\"{$urlPath}\">{$urlPath}</a></p>";
        echo "<p>이 URL로 접근이 가능하므로, 예를 들어 webshell.php 같은 파일을 업로드하면 바로 실행될 수 있습니다.</p>";
    } else {
        echo "Move failed";
    }

    exit;
}
?>
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Vuln Upload</title>
</head>
<body>
<h1>취약한 파일 업로드</h1>
<p>아무 파일이나 업로드가 가능하도록 의도적으로 취약하게 구성되어 있습니다.</p>
<form method="POST" enctype="multipart/form-data">
    <input type="file" name="file"><br>
    <button type="submit">업로드</button>
</form>
<p><a href="posts.php">게시판으로 돌아가기</a></p>
</body>
</html>

