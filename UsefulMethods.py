import discord

async def create_embed(
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
    if author is not None:
        em.set_author(name=author.display_name,icon_url=author.display_avatar)
    if image is not None:
        em.set_image(url=image)
    if thumbnail is not None:
        em.set_thumbnail(url=thumbnail)
    if footer_img is not None and footer_text is not None:
        em.set_footer(text=footer_text,icon_url=footer_img)
    elif footer_img is not None:
        em.set_footer(icon_url=footer_img)
    elif footer_text is not None:
        em.set_footer(text=footer_text)
    
    return em