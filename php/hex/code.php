<?php

$i = 0;
while (true) {
    $get_val = 'hex' . $i;
    if (isset($_GET[$get_val])) {
        $i++;
    } else {
        break;
    }
}

define("BOX_X", 1);
define("BOX_WIDTH", 500);
define("BOX_HEIGHT", 80);
define("WIDTH", BOX_X * BOX_WIDTH);
define("HEIGHT", $i * BOX_HEIGHT);

// Make the image
$img_hex = imagecreatetruecolor(WIDTH, HEIGHT);
imagealphablending($img_hex, true);
// Set colors
$background = imagecolorallocate($img_hex, 255, 255, 255);
$text_color_light = imagecolorallocate($img_hex, 230, 230, 230);
$text_color_dark = imagecolorallocate($img_hex, 24, 24, 24);
imagefill($img_hex, 0, 0, $background);

$i = 0;
while (true) {
    $get_val = 'hex' . $i;
    if (isset($_GET[$get_val])) {
        $hex_raw = $_GET[$get_val];
        $hex_value = "#" . $hex_raw;
        list($r, $g, $b) = sscanf($hex_raw, "%02x%02x%02x");
        $hex_color = imagecolorallocate($img_hex, $r, $g, $b);
        $hex_brightness = ($r + $g + $b) / (255 * 3);

        $box_x = 0;
        $box_y = $i * BOX_HEIGHT;

        imagefilledrectangle($img_hex, $box_x, $box_y, $box_x + BOX_WIDTH, $box_y + BOX_HEIGHT, $hex_color);

        $text_color = $hex_brightness > 0.5 ? $text_color_dark : $text_color_light;

        // Text
        $size = BOX_HEIGHT * 0.5; $font = "Open Sans 600.ttf";
        $tb = imagettfbbox($size, 0, $font, $hex_value);
        //$tx = (($tb[0] - $tb[4]) / 2) + $box_x + (BOX_WIDTH / 2);
        $tx = BOX_WIDTH * 0.04;
        $ty = (($tb[1] - $tb[5]) / 2) + $box_y + (BOX_HEIGHT / 2);
        imagettftext($img_hex, $size, 0, $tx, $ty, $text_color, $font, $hex_value);

        imagecolordeallocate($img_hex, $hex_color);
    } else {
        break;
    }

    $i++;
}

// Serve the image
header("Content-type: image/png");
imagepng($img_hex);

// Free memory
imagecolordeallocate($img_hex, $background);
imagecolordeallocate($img_hex, $text_color_light);
imagecolordeallocate($img_hex, $text_color_dark);
imagedestroy($img_hex);
?>
