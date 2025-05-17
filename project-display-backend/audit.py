import os
import base64
from dotenv import load_dotenv
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException

# 导入文本审核模块和模型
from tencentcloud.tms.v20201229 import tms_client, models

load_dotenv()

def text_moderation_sdk(text):
    try:
        secret_id = os.getenv("SECRET_ID") or ""
        secret_key = os.getenv("SECRET_KEY") or ""
        region = "ap-guangzhou"
        
        cred = credential.Credential(secret_id, secret_key)
        client = tms_client.TmsClient(cred, region)
        req = models.TextModerationRequest()
        
        # 将文本先utf-8编码再base64编码，得到字符串
        encoded_text = base64.b64encode(text.encode('utf-8')).decode('utf-8')
        req.Content = encoded_text
        
        resp = client.TextModeration(req)
        return resp.to_json_string()

    except TencentCloudSDKException as err:
        return f"调用出错: {err}"

# 测试调用
if __name__ == "__main__":
    test_text = "傻逼"
    result = text_moderation_sdk(test_text)
    print(result)