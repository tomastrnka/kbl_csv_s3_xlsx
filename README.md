# kbl_csv_s3_xlsx

1) Set up the tables in the UI of input mapping in Keboola
2) Set up the configuration json in the following way:

{
  "parameters": {
    "S3key": "XXXXXXX",
    "S3secretKey":"XXXXXXXXX",
    "bucketName":"XXXXXXXXXX"
  }
}

3) The component will then take all the input tables, transforms them into .xlsx files and uploads to S3 accordingly to your json settings.
