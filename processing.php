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


// $output = shell_exec('
// export PATH=/sbin:/bin:/usr/sbin:/usr/bin:/usr/local/sbin:/usr/local/bin:/root/bin;
// python pythoncalendar_v3.py 2>&1;
// echo "<br>";
// ');
// $out = var_export($output, true);
// echo $out;

echo "Cal Authentication";
echo "<br>";
$output = shell_exec('
export PATH=/sbin:/bin:/usr/sbin:/usr/bin:/usr/local/sbin:/usr/local/bin:/root/bin;
python calauth.py ' . $initials . ' /usr/local/www/apache24/data/pycalauth/client_secret_728152513941-7ofhna8hvhfcj68nr88sjkoeq7oabcup.apps.googleusercontent.com.json 2>&1;'
);
$out = var_export($output, true);
echo $out;
echo "<br>";
echo "<br>";



echo "Sheet Authentication";
echo "<br>";
$output = shell_exec('
export PATH=/sbin:/bin:/usr/sbin:/usr/bin:/usr/local/sbin:/usr/local/bin:/root/bin;
python sheetauth.py ' . $initials . ' /usr/local/www/apache24/data/pycalauth/client_secret_145372556979-b6di5pm67tdbpmipr6al0mein5eeq1aq.apps.googleusercontent.com.json 2>&1;'
);
$out = var_export($output, true);
echo $out;
echo"<br>";


?>