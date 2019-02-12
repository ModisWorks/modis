import discord

cmd_db = {}

perm_db = {
    "administrator": discord.Permissions(8),
    "view_audit_logs": discord.Permissions(128),
    "manage_server": discord.Permissions(32),
    "manage_roles": discord.Permissions(268435456),
    "manage_channels": discord.Permissions(16),
    "kick_members": discord.Permissions(2),
    "ban_members": discord.Permissions(4),
    "create_instant_invite": discord.Permissions(1),
    "change_nickname": discord.Permissions(67108864),
    "manage_nicknames": discord.Permissions(134217728),
    "manage_emojis": discord.Permissions(1073741824),
    "manage_webhooks": discord.Permissions(536870912),
    "view_channels": discord.Permissions(1024),
    "send_messages": discord.Permissions(2048),
    "seng_tts_messages": discord.Permissions(4096),
    "manage_messages": discord.Permissions(8192),
    "embed_links": discord.Permissions(16384),
    "attach_files": discord.Permissions(32768),
    "read_message_history": discord.Permissions(65536),
    "mention_everyone": discord.Permissions(131072),
    "use_external_emojis": discord.Permissions(262144),
    "add_reactions": discord.Permissions(64),
    "connect": discord.Permissions(1048576),
    "speak": discord.Permissions(2097152),
    "mute_members": discord.Permissions(4194304),
    "deafen_members": discord.Permissions(8388608),
    "use_members": discord.Permissions(16777216),
    "use_voice_activation": discord.Permissions(33554432),
    "priority_speaker": discord.Permissions(256)
}