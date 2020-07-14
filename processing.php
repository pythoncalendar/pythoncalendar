<?php


$calendar_colors = [
    "Lavender"  => 1,
    "Sage"      => 2,
    "Grape"     => 3,
    "Flamingo"  => 4,
    "Banana"    => 5,
    "Tangerine" => 6,
    "Peacock"   => 7,
    "Grapite"   => 8,
    "Blueberry" => 9,
    "Basil"     => 10,
    "Tomato"    => 11,
];

$cal_color = $calendar_colors[$_POST['cal_color']];
$initials = $_POST['initals'];
$email = $_POST['email'];
$string = "Kachow!";
$myfile = fopen("list.py", "w") or die("Unable to open file!");
fwrite($myfile, $string);


echo "Hello all";
echo "<br>";


$output = shell_exec('
export PATH=/sbin:/bin:/usr/sbin:/usr/bin:/usr/local/sbin:/usr/local/bin:/root/bin;
python pythoncalendar_v3.py 2>&1;
echo "done";
');
$out = var_export($output, true);
echo $out;

?>