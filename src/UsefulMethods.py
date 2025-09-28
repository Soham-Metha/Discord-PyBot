import discord

def create_embed(
    title:str,desc: str,
    url: str=None, 
    author: discord.Member = None,
    image:str=None,
    thumbnail:str=None,
    footer_img:str=None,
    footer_text:str=None
    ):
    """
    create an embed
    """
    em= discord.Embed(title=title,color=discord.Colour.blurple(),description=desc,url=url)
    em.set_author(name=author.display_name,icon_url=author.display_avatar)
    em.set_image(url=image)
    em.set_thumbnail(url=thumbnail)
    em.set_footer(icon_url=footer_img)
    em.set_footer(text=footer_text)
    
    return em