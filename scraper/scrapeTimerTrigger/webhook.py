import requests as r
import json


def construct_json(deal_obj):
    json_dict = {
        "content": f"<@{deal_obj.discord_id}>",
        "embeds":   [
                {
                    "title": "DEAL FOUND!",
                    "description": f"**{deal_obj.name}**\n¥ {deal_obj.listing_price_cny} (~{round(deal_obj.listing_price_eur, 2)} €)\nFloat value: {deal_obj.float_val}\nApproximate profit margin: {round(deal_obj.median_price / deal_obj.listing_price_cny - 100, 2)}%\n\n{deal_obj.purchase_url}",
                    "color": "4718336",
                    "image": {
                        "url": str(deal_obj.screenshot_url),
                    }
                }
            ],
    }
    print(json_dict)
    return json.dumps(json_dict)


def notify_user(json_info):
    url = "https://discord.com/api/webhooks/1102264908067913768/RBB0Rd1zGAlfVbFCx3kz_5CRL7r4YT2T0Vt5FU_IH22u7genpNV2iVgI_faMu6ygvwha"
    headers = {
        "Content-Type": "application/json",
    }
    response = r.post(url=url, data=json_info, headers=headers)
    print(response.text)
