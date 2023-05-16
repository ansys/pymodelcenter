"""Provides a reusable way to patch client creation on gRPC-based PyModelCenter classes."""


def monkeypatch_client_creation(
    mpatch_or_context, target_class, mock_client, client_creation_func="_create_client"
):
    """
    Monkeypatch a test implementation type.

    :param mpatch_or_context: either the monkeypatch object provided by pytest,
        or a monkeypatch context object during the lifespan of which the patch will apply.
    :param target_class: the class to monkeypatch. This should be the implementation class
        from grpc_modelcenter that is under test. The class should have a method it uses
        to create a client from a grpc channel that can be replaced.
    :param mock_client: the mock client to return
    :param client_creation_func: the name of the method to patch.
    """
    # Create a lambda that returns the mock client.
    mock_client_create = lambda obj, channel, mock_client=mock_client: mock_client

    # Monkeypatch the target type.
    mpatch_or_context.setattr(target_class, client_creation_func, mock_client_create)
