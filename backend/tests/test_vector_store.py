import pytest
from unittest.mock import patch, MagicMock

@patch('app.db.vector_store.Pinecone')
def test_pinecone_init(mock_pinecone):
    # Mock Pinecone to avoid actual API calls during basic tests
    mock_pc_instance = MagicMock()
    mock_pinecone.return_value = mock_pc_instance
    
    # We delay import so the mock takes effect before the instance is created
    from backend.app.db.vector_store import PineconeStore
    
    # Assuming config is loaded, we can just instantiate it
    store = PineconeStore()
    
    assert store.dimension == 1024
    mock_pinecone.assert_called_once()
