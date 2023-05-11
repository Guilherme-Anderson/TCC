<?php

if(isset($_GET["bancada"]) ) {
   $bancada = $_GET["bancada"]; // get temperature value from HTTP GET
   $leitura1 = $_GET["leitura1"];
   $leitura2 = $_GET["leitura2"];

   $servername = "localhost";
   $username = "ESP32";
   $password = "esp32io.com";
   $database_name = "test";

   // Create MySQL connection fom PHP to MySQL server
   $connection = new mysqli($servername, $username, $password, $database_name);
   // Check connection
   if ($connection->connect_error) {
      die("MySQL connection failed: " . $connection->connect_error);
   }

   $sql = "INSERT INTO test.leitura (bancada,leitura1,leitura2) VALUES ('$bancada','$leitura1','$leitura2')";

   if ($connection->query($sql) === TRUE) {
      echo "New record created successfully";
   } else {
      echo "Error: " . $sql . " => " . $connection->error;
   }

   $connection->close();
} else {
   echo "temperature is not set in the HTTP request";
}
?>
