import unittest
from unittest.mock import patch, MagicMock
import lambda_function

class TestLambdaPipeline(unittest.TestCase):

    @patch('lambda_function.s3_client')
    @patch('lambda_function.table')
    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data="id,name,age\n1,Anil,25\n2,John,30")
    @patch('os.path.basename')
    def test_lambda_handler_success(self, mock_basename, mock_file_open, mock_dynamo_table, mock_s3):
        # Arrange mock configurations
        mock_basename.return_value = "dataset.csv"
        
        # Simulate standard AWS S3 Put Event template payload
        mock_event = {
            "Records": [{
                "s3": {
                    "bucket": {"name": "assignment-pipeline-ingest-anil"},
                    "object": {
                        "key": "dataset.csv",
                        "size": 183
                    }
                }
            }]
        }
        
        # Act
        response = lambda_function.lambda_handler(mock_event, None)
        
        # Assert S3 verification downloads happened correctly
        mock_s3.download_file.assert_called_once_with("assignment-pipeline-ingest-anil", "dataset.csv", "/tmp/dataset.csv")
        
        # Assert database updates executed
        mock_dynamo_table.put_item.assert_called_once()
        called_item = mock_dynamo_table.put_item.call_args[1]['Item']
        
        self.assertEqual(called_item['file_name'], 'dataset.csv')
        self.assertEqual(called_item['columns'], 3)
        self.assertEqual(called_item['file_size_bytes'], 183)
        self.assertEqual(response['statusCode'], 200)

if __name__ == '__main__':
    unittest.main()
