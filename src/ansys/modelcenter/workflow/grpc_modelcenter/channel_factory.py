import grpc


class ChannelFactory:
    """Provides methods for creating a gRPC channel to pass to an Engine object."""

    @staticmethod
    def create_channel(
            host: str,
            port: int):
        """Create a new channel using WNUA for authentication.

        Parameters
        ----------
        host : str
            The host to connect to.
        port: int
            The port to connect to.
        """
        options = (('grpc.default_authority', 'localhost'),)
        channel = grpc.insecure_channel(f"{host}:{port}", options=options)
        return channel