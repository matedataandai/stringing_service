import streamlit as st
import streamlit.components.v1 as components
import boto3
import json

client = boto3.client("secretsmanager", region_name="ap-southeast-2")
response = client.get_secret_value(SecretId="restring_secrets")
secrets_aws = json.loads(response["SecretString"])

def inject_meta_pixel():
    pixel_id = secrets_aws.get("META_PIXEL_ID")
    """Injects the Meta Pixel base code into a Streamlit app."""
    pixel_code = f"""
    <!-- Meta Pixel Code -->
    <script>
    !function(f,b,e,v,n,t,s)
    {{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?
    n.callMethod.apply(n,arguments):n.queue.push(arguments)}};
    if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
    n.queue=[];t=b.createElement(e);t.async=!0;
    t.src=v;s=b.getElementsByTagName(e)[0];
    s.parentNode.insertBefore(t,s)}}(window, document,'script',
    'https://connect.facebook.net/signals/js/fbq.js');
    
    fbq('init', '{pixel_id}');
    fbq('track', 'PageView');
    </script>
    <noscript><img height="1" width="1" style="display:none"
    src="https://www.facebook.com/tr?id={pixel_id}&ev=PageView&noscript=1"
    /></noscript>
    <!-- End Meta Pixel Code -->
    """
    
    # Render the component (height=0 keeps it invisible)
    components.html(pixel_code, height=0, width=0)
