from utils.constants import CHARSET, CONFIGURATION, REGION, SENDER, SERVICE
import logging
from typing import Any, List

import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


class BaseConfig:
    def __init__(
        self,
        service: str,
        region: str,
        sender: str,
        configuration: str,
        charset: str,
    ) -> None:
        self.service = service
        self.region = region
        self.sender = sender
        self.configuration = configuration
        self.charset = charset


class DefaultConfig(BaseConfig):
    def __init__(self) -> None:
        super().__init__(
            service=SERVICE,
            region=REGION,
            sender=SENDER,
            configuration=CONFIGURATION,
            charset=CHARSET
        )


class Communication:

    def __init__(self) -> None:
        self._config = DefaultConfig()

    @property
    def client(self) -> Any:
        return boto3.client(
            self._config.service, region_name=self._config.region
        )

    def send(
        self,
        *,
        recipients: List[str],
        template: str,
        text: str,
        subject: str
    ) -> None:
        """Send email notifications to several recipients"""

        try:
            self.client.send_email(
                Destination={
                    'ToAddresses': recipients,
                },
                Message={
                    'Body': {
                        'Html': {
                            'Charset': self._config.charset,
                            'Data': template,
                        },
                        'Text': {
                            'Charset': self._config.charset,
                            'Data': text,
                        },
                    },
                    'Subject': {
                        'Charset': self._config.charset,
                        'Data': subject,
                    },
                },
                Source=self._config.sender,
                ConfigurationSetName=self._config.configuration,
            )
        except ClientError as err:
            logger.error(f'send :: error :: {err}')
