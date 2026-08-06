<?php
if (isset($_SERVER['PATH_INFO']) && $_SERVER['PATH_INFO'] !== '') {
    http_response_code(404);
    echo "Not Found";
    exit;
}
echo "Secret data: FLAG{this_is_a_flag}";
?>
