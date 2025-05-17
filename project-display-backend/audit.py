import json
import os
import base64
from dotenv import load_dotenv
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException

# 导入文本审核模块和模型
from tencentcloud.tms.v20201229 import tms_client, models
# 导入内容安全服务的图片审核模块和模型
from tencentcloud.cms.v20190321 import cms_client, models

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
        return json.dumps({"Suggestion": "Pass"})
      
def image_moderation_sdk(image_path):
    try:
        secret_id = os.getenv("SECRET_ID") or ""
        secret_key = os.getenv("SECRET_KEY") or ""
        region = "ap-guangzhou"

        cred = credential.Credential(secret_id, secret_key)
        client = cms_client.CmsClient(cred, region)

        with open(image_path, "rb") as f:
            img_data = f.read()
        encoded_image = base64.b64encode(img_data).decode()

        req = models.ImageModerationRequest()
        req.FileContent = encoded_image

        resp = client.ImageModeration(req)
        return resp.to_json_string()

    except TencentCloudSDKException as err:
        return json.dumps({"Suggestion": "Pass"})

# 测试调用
if __name__ == "__main__":
    test_text = "测试文本"
    result = text_moderation_sdk(test_text)
    print(result)
    test_image_path = "./defaultImage/1.png"
    result = image_moderation_sdk(test_image_path)
    print(result)