# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from dataclasses import dataclass, field
from enum import IntEnum
from typing import AsyncGenerator, overload, TYPE_CHECKING

from .invite import Invite
from .channel import Channel
from ..message.emoji import Emoji
from ..message.file import File
from ...exceptions import UnavailableGuildError
from ...utils.api_object import APIObject
from ...utils.conversion import construct_client_dict, remove_none
from ...utils.types import MISSING


if TYPE_CHECKING:
    from typing import Any, Dict, List, Optional, Union

    from .audit_log import AuditLog
    from .ban import Ban
    from .member import GuildMember
    from .features import GuildFeature
    from .role import Role
    from .stage import StageInstance
    from .template import GuildTemplate
    from .welcome_screen import WelcomeScreen, WelcomeScreenChannel
    from .widget import GuildWidget
    from .webhook import Webhook
    from ..user.user import User
    from ..user.integration import Integration
    from ..voice.region import VoiceRegion
    from ..events.presence import PresenceUpdateEvent
    from ..message.sticker import Sticker
    from ..user.voice_state import VoiceState
    from ...client import Client
    from ...utils.timestamp import Timestamp
    from ...utils.types import APINullable, JSONSerializable
    from ...utils.snowflake import Snowflake


class PremiumTier(IntEnum):
    """Represents the boost tier of a guild.
    Attributes
    ----------
    NONE:
        Guild has not unlocked any Server Boost perks.
    TIER_1:
        Guild has unlocked Server Boost level 1 perks.
    TIER_2:
        Guild has unlocked Server Boost level 2 perks.
    TIER_3:
        Guild has unlocked Server Boost level 3 perks.
    """

    NONE = 0
    TIER_1 = 1
    TIER_2 = 2
    TIER_3 = 3


class GuildNSFWLevel(IntEnum):
    """Represents the NSFW level of a guild.
    Attributes
    ----------
    DEFAULT:
        Default NSFW level.
    EXPLICIT:
        Explicit NSFW level.
    SAFE:
        SAFE NSFW level.
    AGE_RESTRICTED:
        Age restricted NSFW level.
    """

    DEFAULT = 0
    EXPLICIT = 1
    SAFE = 2
    AGE_RESTRICTED = 3


class ExplicitContentFilterLevel(IntEnum):
    """Represents the filter content level of a guild.
    Attributes
    ----------
    DISABLED:
        Media content will not be scanned.
    MEMBERS_WITHOUT_ROLES:
        Media content sent by members without roles will be scanned.
    ALL_MEMBERS:
        Media content sent by all members will be scanned.
    """

    DISABLED = 0
    MEMBERS_WITHOUT_ROLES = 1
    ALL_MEMBERS = 2


class MFALevel(IntEnum):
    """Represents the multi factor authentication level of a guild.
    Attributes
    ----------
    NONE:
        Guild has no MFA/2FA requirement for moderation actions.
    ELEVATED:
        Guild has a 2FA requirement for moderation actions
    """

    NONE = 0
    ELEVATED = 1


class VerificationLevel(IntEnum):
    """Represents the verification level of a guild.
    Attributes
    ----------
    NONE:
        Unrestricted.
    LOW:
        Must have verified email on account.
    MEDIUM:
        Must be registered on Discord for longer than 5 minutes.
    HIGH:
        Must be a member of the server for longer than 10 minutes.
    VERY_HIGH:
        Must have a verified phone number.
    """

    NONE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    VERY_HIGH = 4


class DefaultMessageNotificationLevel(IntEnum):
    """Represents the default message notification level of a guild.
    Attributes
    ----------
    ALL_MESSAGES:
        Members will receive notifications for all messages by default.
    ONLY_MENTIONS:
        Members will receive notifications only for messages that @mention them by default.
    """

    # noqa: E501
    ALL_MESSAGES = 0
    ONLY_MENTIONS = 1


class SystemChannelFlags(IntEnum):
    """Represents the system channel flags of a guild.
    Attributes
    ----------
    SUPPRESS_JOIN_NOTIFICATIONS:
        Suppress member join notifications.
    SUPPRESS_PREMIUM_SUBSCRIPTIONS:
        Suppress server boost notifications.
    SUPPRESS_GUILD_REMINDER_NOTIFICATIONS:
        Suppress server setup tips.
    SUPPRESS_JOIN_NOTIFICATION_REPLIES:
        Hide member join sticker reply buttons
    """

    SUPPRESS_JOIN_NOTIFICATIONS = 1 << 0
    SUPPRESS_PREMIUM_SUBSCRIPTIONS = 1 << 1
    SUPPRESS_GUILD_REMINDER_NOTIFICATIONS = 1 << 2
    SUPPRESS_JOIN_NOTIFICATION_REPLIES = 1 << 3



@dataclass(repr=False)
class GuildPreview(APIObject):
    """Represents a guild preview.
    Attributes
    ----------
    id: :class:`Snowflake`
        The guild ID.
    name: :class:`str`
        The guild name.
    icon: :class:`str`
        The guild icon hash.
    splash: :class:`str`
        The guild splash hash.
    discovery_splash: :class:`str`
        The guild discovery splash hash.
    emojis: :class:`List[Emoji]`
        The guild emojis.
    features: :class:`List[GuildFeature]`
        The guild features.
    approximate_member_count: :class:`int`
        The approximate member count.
    approximate_presence_count: :class:`int`
        The approximate number of online members in this guild
    description: :class:`str`
        The guild description.
    """

    id: Snowflake
    name: str
    emojis: List[Emoji]
    features: List[GuildFeature]
    approximate_member_count: int
    approximate_presence_count: int

    icon: APINullable[str] = MISSING
    splash: APINullable[str] = MISSING
    discovery_splash: APINullable[str] = MISSING
    description: APINullable[str] = MISSING


@dataclass(repr=False)
class Guild(APIObject):
    """Represents a Discord guild/server in which your client resides.
    Attributes
    ----------
    afk_channel_id: Optional[:class:`~pincer.utils.snowflake.Snowflake`]
        Id of afk channel
    afk_timeout: :class:`int`
        Afk timeout in seconds
    application_id: Optional[:class:`~pincer.utils.snowflake.Snowflake`]
        Application id of the guild creator if it is bot-created
    banner: Optional[:class:`str`]
        Banner hash
    default_message_notifications: :class:`~pincer.objects.guild.guild.DefaultMessageNotificationLevel`
        Default message notifications level
    description: Optional[:class:`str`]
        The description of a Community guild
    discovery_splash: Optional[:class:`str`]
        Discovery splash hash;
        only present for guilds with the "DISCOVERABLE" feature
    emojis: List[:class:`~pincer.objects.message.emoji.Emoji`]
        Custom guild emojis
    explicit_content_filter: :class:`~pincer.objects.guild.guild.ExplicitContentFilterLevel`
        Explicit content filter level
    features: List[:class:`~pincer.objects.guild.features.GuildFeature`]
        Enabled guild features
    id: :class:`~pincer.utils.snowflake.Snowflake`
        Guild id
    icon: Optional[:class:`str`]
        Icon hash
    mfa_level: :class:`~pincer.objects.guild.guild.MFALevel`
        Required MFA level for the guild
    name: :class:`str`
        Guild name (2-100 characters, excluding trailing and leading
        whitespace)
    nsfw_level: :class:`~pincer.objects.guild.guild.NSFWLevel`
        Guild NSFW level
    owner_id: :class:`~pincer.utils.snowflake.Snowflake`
        Id of owner
    preferred_locale: :class:`str`
        The preferred locale of a Community guild;
        used in server discovery and notices from Discord;
        defaults to "en-US"
    premium_tier: :class:`~pincer.objects.guild.guild.PremiumTier`
        Premium tier (Server Boost level)
    public_updates_channel_id: Optional[:class:`~pincer.utils.snowflake.Snowflake`]
        The id of the channel where admins
        and moderators of Community guilds receive notices from Discord
    roles: List[:class:`~pincer.objects.guild.role.Role`]
        Roles in the guild
    rules_channel_id: Optional[:class:`~pincer.utils.snowflake.Snowflake`]
        The id of the channel where Community guilds can display rules
        and/or guidelines
    splash: Optional[:class:`str`]
        Splash hash
    system_channel_flags: :class:`~pincer.objects.guild.guild.SystemChannelFlags`
        System channel flags
    system_channel_id: Optional[:class:`~pincer.utils.snowflake.Snowflake`]
        The id of the channel where guild notices
        such as welcome messages and boost events are posted
    vanity_url_code: Optional[:class:`str`]
        The vanity url code for the guild
    verification_level: :class:`~pincer.objects.guild.guild.VerificationLevel`
        Verification level required for the guild
    approximate_member_count: APINullable[:class:`int`]
        Approximate number of members in this guild, returned from the
        `GET /guilds/<id>` endpoint when with_counts is true
    approximate_presence_count: APINullable[:class:`int`]
        Approximate number of non-offline members in this guild,
        returned from the `GET /guilds/<id>`
        endpoint when with_counts is true
    channels: APINullable[List[:class:`~pincer.objects.guild.channel.Channel`]]
        Channels in the guild
    icon_hash: APINullable[Optional[:class:`str`]]
        Icon hash, returned when in the template object
    joined_at: APINullable[:class:`~pincer.utils.timestamp.Timestamp`]
        When this guild was joined at
    large: APINullable[:class:`bool`]
        True if this is considered a large guild
    max_members: APINullable[:class:`int`]
        The maximum number of members for the guild
    max_presences: APINullable[Optional[:class:`int`]]
        The maximum number of presences for the guild
        (null is always returned, apart from the largest of guilds)
    max_video_channel_users: APINullable[:class:`int`]
        The maximum amount of users in a video channel
    members: APINullable[List[:class:`~pincer.objects.guild.member.GuildMember`]]
        Users in the guild
    member_count: APINullable[:class:`bool`]
        Total number of members in this guild
    nsfw: APINullable[:class:`bool`]
        Boolean if the server is NSFW
    owner: APINullable[:class:`bool`]
        True if the user is the owner of the guild
    permissions: APINullable[:class:`str`]
        Total permissions for the user in the guild
        (excludes overwrites)
    premium_subscription_count: APINullable[:class:`int`]
        The number of boosts this guild currently has
    presences: APINullable[List[:class:`~pincer.objects.events.presence.PresenceUpdateEvent`]]
        Presences of the members in the guild,
        will only include non-offline members if the size is greater
        than large threshold
    stage_instances: APINullable[List[:class:`~pincer.objects.guild.stage.StageInstance`]]
        Stage instances in the guild
    stickers: Optional[List[:class:`~pincer.objects.message.sticker.Sticker`]]
        Custom guild stickers
    region: APINullable[Optional[:class:`str`]]
        Voice region id for the guild (deprecated)
    threads: APINullable[List[:class:`~pincer.objects.guild.channel.Channel`]]
        All active threads in the guild that current user
        has permission to view
    unavailable: APINullable[:class:`bool`]
        True if this guild is unavailable due to an outage
    voice_states: APINullable[List[:class:`~pincer.objects.user.voice_state.VoiceState`]]
        States of members currently in voice channels;
        lacks the guild_id key
    widget_enabled: APINullable[:class:`bool`]
        True if the server widget is enabled
    widget_channel_id: APINullable[Optional[:class:`~pincer.utils.snowflake.Snowflake`]]
        The channel id that the widget will generate an invite to,
        or null if set to no invite
    welcome_screen: APINullable[:class:`~pincer.objects.guild.welcome_screen.WelcomeScreen`]
        The welcome screen of a Community guild, shown to new members,
        returned in an Invite's guild object
    """

    # noqa: E501
    features: List[GuildFeature]
    id: Snowflake
    name: str
    nsfw_level: GuildNSFWLevel
    verification_level: VerificationLevel

    # Guild invites missing
    system_channel_flags: APINullable[SystemChannelFlags] = MISSING
    explicit_content_filter: APINullable[ExplicitContentFilterLevel] = MISSING
    premium_tier: APINullable[PremiumTier] = MISSING
    default_message_notifications: APINullable[DefaultMessageNotificationLevel] = MISSING
    mfa_level: APINullable[MFALevel] = MISSING
    owner_id: APINullable[Snowflake] = MISSING
    afk_timeout: APINullable[int] = MISSING
    emojis: APINullable[List[Emoji]] = MISSING
    preferred_locale: APINullable[str] = MISSING
    roles: APINullable[List[Role]] = MISSING

    guild_scheduled_events: APINullable[List] = MISSING
    lazy: APINullable[bool] = MISSING
    premium_progress_bar_enabled: APINullable[bool] = MISSING
    guild_hashes: APINullable[Dict] = MISSING
    afk_channel_id: APINullable[Snowflake] = MISSING
    application_id: APINullable[Snowflake] = MISSING
    embedded_activities: APINullable[List] = MISSING
    banner: APINullable[str] = MISSING
    description: APINullable[str] = MISSING
    discovery_splash: APINullable[str] = MISSING
    icon: APINullable[str] = MISSING
    public_updates_channel_id: APINullable[Snowflake] = MISSING
    rules_channel_id: APINullable[Snowflake] = MISSING
    splash: APINullable[str] = MISSING
    system_channel_id: APINullable[Snowflake] = MISSING
    vanity_url_code: APINullable[str] = MISSING

    application_command_counts: APINullable[Dict] = MISSING
    application_command_count: APINullable[int] = MISSING
    approximate_member_count: APINullable[int] = MISSING
    approximate_presence_count: APINullable[int] = MISSING
    channels: APINullable[List[Channel]] = field(default_factory=list)
    # TODO: Add type when type is known
    hub_type: APINullable[Any] = MISSING
    icon_hash: APINullable[Optional[str]] = MISSING
    joined_at: APINullable[Timestamp] = MISSING
    large: APINullable[bool] = MISSING
    max_members: APINullable[int] = MISSING
    max_presences: APINullable[Optional[int]] = MISSING
    max_video_channel_users: APINullable[int] = MISSING
    members: APINullable[List[GuildMember]] = MISSING
    member_count: APINullable[bool] = MISSING
    nsfw: APINullable[bool] = MISSING
    # Note: This is missing from discord's docs but in the api
    owner: APINullable[bool] = MISSING
    permissions: APINullable[str] = MISSING
    premium_subscription_count: APINullable[int] = MISSING
    presences: APINullable[List[PresenceUpdateEvent]] = MISSING
    stage_instances: APINullable[List[StageInstance]] = MISSING
    stickers: APINullable[List[Sticker]] = MISSING
    region: APINullable[Optional[str]] = MISSING
    threads: APINullable[List[Channel]] = MISSING
    # Guilds are considered available unless otherwise specified
    unavailable: APINullable[bool] = False
    voice_states: APINullable[List[VoiceState]] = MISSING
    widget_enabled: APINullable[bool] = MISSING
    widget_channel_id: APINullable[Optional[Snowflake]] = MISSING
    welcome_screen: APINullable[WelcomeScreen] = MISSING

    @classmethod
    async def from_id(cls, client: Client, _id: Union[int, Snowflake]) -> Guild:
        """
        Parameters
        ----------
        client : `~pincer.Client`
            Client object to use the http gateway from.
        _id : :class: `pincer.utils.snowflake.Snowflake`
            Guild ID.
        Returns
        -------
        :class: `~pincer.objects.guild.guild.Guild`
            The new guild object.
        """
        data = await client.http.get(f"/guilds/{_id}")
        channel_data = await client.http.get(f"/guilds/{_id}/channels")

        data["channels"]: List[Channel] = [
            Channel.from_dict(construct_client_dict(client, i))
            for i in (channel_data or [])
        ]

        return Guild.from_dict(construct_client_dict(client, data))

    async def get_member(self, _id: int) -> GuildMember:
        """|coro|
        Fetches a GuildMember from its identifier

        Parameters
        ----------
        _id: int
            The id of the guild member which should be fetched from the Discord
            gateway.
        Returns
        -------
        :class:`~pincer.objects.guild.member.GuildMember`
            A GuildMember object.
        """
        return await GuildMember.from_id(self._client, self.id, _id)

    @overload
    async def modify_member(
        self,
        *,
        _id: int,
        nick: Optional[str] = None,
        roles: Optional[List[Snowflake]] = None,
        mute: Optional[bool] = None,
        deaf: Optional[bool] = None,
        channel_id: Optional[Snowflake] = None,
    ) -> GuildMember:
        """|coro|
        Modifies a member in the guild from its identifier and based on the
        keyword arguments provided.
        Parameters
        ----------
        _id : int
            Id of the member to modify
        nick : Optional[:class:`str`]
            New nickname for the member |default| :data:`None`
        roles : Optional[List[:class:`~pincer.utils.snowflake.Snowflake]]
            New roles for the member |default| :data:`None`
        mute : Optional[:class:`bool`]
            Whether the member is muted |default| :data:`None`
        deaf : Optional[:class:`bool`]
            Whether the member is deafened |default| :data:`None`
        channel_id : Optional[:class:`~pincer.utils.snowflake.Snowflake]
            Voice channel id to move to |default| :data:`None`
        Returns
        -------
        :class:`~pincer.objects.guild.member.GuildMember`
            The new member object.
        """
        ...

    async def modify_member(self, _id: int, **kwargs) -> GuildMember:
        data = await self._http.patch(
            f"guilds/{self.id}/members/{_id}", data=kwargs
        )
        return GuildMember.from_dict(construct_client_dict(self._client, data))

    async def ban(
        self,
        member_id: int,
        reason: str = None,
        delete_message_days: int = None
    ):
        """
        Parameters
        ----------
        member_id : :class:`int`
            ID of the guild member to ban.
        reason : Optional[:class:`str`]
            Reason for the kick.
        delete_message_days : Optional[:class:`int`]
            Number of days to delete messages for (0-7)
        """
        headers = {}

        if reason is not None:
            headers["X-Audit-Log-Reason"] = reason

        data = {}

        if delete_message_days is not None:
            data["delete_message_days"] = delete_message_days

        await self._http.put(
            f"/guilds/{self.id}/bans/{member_id}",
            data=data,
            headers=headers
        )

    async def kick(self, member_id: int, reason: Optional[str] = None):
        """|coro|
        Kicks a guild member.
        Parameters
        ----------
        member_id : :class:`int`
            ID of the guild member to kick.
        reason : Optional[:class:`str`]
            Reason for the kick.
        """

        headers = {}

        if reason is not None:
            headers["X-Audit-Log-Reason"] = reason

        await self._http.delete(
            f"/guilds/{self.id}/members/{member_id}",
            header=headers
        )

    async def get_roles(self) -> AsyncGenerator[Role, None]:
        """|coro|
        Fetches all the roles in the guild.

        Yields
        -------
        AsyncGenerator[:class:`~pincer.objects.guild.role.Role`, :data:`None`]
            An async generator of Role objects.
        """
        data = await self._http.get(f"guilds/{self.id}/roles")
        for role_data in data:
            yield Role.from_dict(construct_client_dict(self._client, role_data))

    @overload
    async def create_role(
        self,
        reason: Optional[str] = None,
        *,
        name: Optional[str] = "new role",
        permissions: Optional[str] = None,
        color: Optional[int] = 0,
        hoist: Optional[bool] = False,
        icon: Optional[str] = None,
        unicode_emoji: Optional[str] = None,
        mentionable: Optional[bool] = False,
    ) -> Role:
        """|coro|
        Creates a new role for the guild.
        Requires the ``MANAGE_ROLES`` permission.

        Parameters
        ----------
        reason : Optional[:class:`str`]
            Reason for creating the role. |default| :data:`None`
        name : Optional[:class:`str`]
            name of the role |default| :data:`"new role"`
        permissions : Optional[:class:`str`]
            bitwise value of the enabled/disabled
            permissions, set to @everyone permissions
            by default |default| :data:`None`
        color : Optional[:class:`int`]
            RGB color value |default| :data:`0`
        hoist : Optional[:class:`bool`]
            whether the role should be displayed
            separately in the sidebar |default| :data:`False`
        icon : Optional[:class:`str`]
            the role's icon image (if the guild has
            the ``ROLE_ICONS`` feature) |default| :data:`None`
        unicode_emoji : Optional[:class:`str`]
            the role's unicode emoji as a standard emoji (if the guild
            has the ``ROLE_ICONS`` feature) |default| :data:`None`
        mentionable : Optional[:class:`bool`]
            whether the role should be mentionable |default| :data:`False`

        Returns
        -------
        :class:`~pincer.objects.guild.role.Role`
            The new role object.
        """
        ...

    async def create_role(
        self,
        reason: Optional[str] = None,
        **kwargs
    ) -> Role:
        return Role.from_dict(
            construct_client_dict(
                self._client,
                await self._http.post(
                    f"guilds/{self.id}/roles",
                    data=kwargs,
                    headers=remove_none({"X-Audit-Log-Reason": reason})
                ),
            )
        )

    async def edit_role_position(
        self,
        id: Snowflake,
        reason: Optional[str] = None,
        position: Optional[int] = None
    ) -> AsyncGenerator[Role, None]:
        """|coro|
        Edits the position of a role.

        Parameters
        ----------
        id : :class:`~pincer.utils.snowflake.Snowflake`
            The role ID
        reason : Optional[:class:`str`]
            Reason for editing the role position. |default| :data:`None`
        position : Optional[:class:`int`]
            Sorting position of the role |default| :data:`None`

        Yields
        -------
        AsyncGenerator[:class:`~pincer.objects.guild.role.Role`, :data:`None`]
            An async generator of all of the guild's role objects.
        """
        data = await self._http.patch(
            f"guilds/{self.id}/roles",
            data={"id": id, "position": position},
            headers=remove_none({"X-Audit-Log-Reason": reason})
        )
        for role_data in data:
            yield Role.from_dict(construct_client_dict(self._client, role_data))

    @overload
    async def edit_role(
        self,
        id: Snowflake,
        reason: Optional[str] = None,
        *,
        name: Optional[str] = None,
        permissions: Optional[str] = None,
        color: Optional[int] = None,
        hoist: Optional[bool] = None,
        icon: Optional[str] = None,
        unicode_emoji: Optional[str] = None,
        mentionable: Optional[bool] = None,
    ) -> Role:
        """|coro|
        Edits a role.
        Requires the ``MANAGE_ROLES`` permission.

        Parameters
        ----------
        id : :class:`~pincer.utils.snowflake.Snowflake`
            The role ID
        reason : Optional[:class:`str`]
            Reason for editing the role |default| :data:`None`
        name : Optional[:class:`str`]
            Name of the role |default| :data:`None`
        permissions : Optional[:class:`str`]
            Bitwise value of the enabled/disabled
            permissions |default| :data:`None`
        color : Optional[:class:`int`]
            RGB color value |default| :data:`None`
        hoist : Optional[:class:`bool`]
            Whether the role should be displayed
            separately in the sidebar |default| :data:`None`
        icon : Optional[:class:`str`]
            The role's icon image (if the guild has
            the ``ROLE_ICONS`` feature) |default| :data:`None`
        unicode_emoji : Optional[:class:`str`]
            The role's unicode emoji as a standard emoji (if the guild
            has the ``ROLE_ICONS`` feature) |default| :data:`None`
        mentionable : Optional[:class:`bool`]
            Whether the role should be mentionable |default| :data:`None`

        Returns
        -------
        :class:`~pincer.objects.guild.role.Role`
            The edited role object.
        """
        ...

    async def edit_role(
        self,
        id: Snowflake,
        reason: Optional[str] = None,
        **kwargs
    ) -> Role:
        return Role.from_dict(
            construct_client_dict(
                self._client,
                await self._http.patch(
                    f"guilds/{self.id}/roles/{id}",
                    data=kwargs,
                    headers=remove_none({"X-Audit-Log-Reason": reason})
                ),
            )
        )

    async def delete_role(self, id: Snowflake, reason: Optional[str] = None):
        """|coro|
        Deletes a role.
        Requires the `MANAGE_ROLES` permission.

        Parameters
        ----------
        id : :class:`~pincer.utils.snowflake.Snowflake`
            The role ID
        reason : Optional[:class:`str`]
            The reason for deleting the role |default| :data:`None`
        """
        await self._http.delete(
            f"guilds/{self.id}/roles/{id}",
            headers=remove_none({"X-Audit-Log-Reason": reason})
        )

    async def get_bans(self) -> AsyncGenerator[Ban, None]:
        """|coro|
        Fetches all the bans in the guild.

        Yields
        -------
        AsyncGenerator[:class:`~pincer.objects.guild.ban.Ban`, :data:`None`]
            An async generator of Ban objects.
        """
        data = await self._http.get(f"guilds/{self.id}/bans")
        for ban_data in data:
            yield Ban.from_dict(construct_client_dict(self._client, ban_data))

    async def get_ban(self, id: Snowflake) -> Ban:
        """|coro|
        Fetches a ban from the guild.

        Parameters
        ----------
        id : :class:`~pincer.utils.snowflake.Snowflake`
            The user ID

        Returns
        -------
        :class:`~pincer.objects.guild.ban.Ban`
            The Ban object.
        """
        return Ban.from_dict(
            construct_client_dict(
                self._client,
                await self._http.get(f"guilds/{self.id}/bans/{id}"),
            )
        )

    async def unban(self, id: Snowflake, reason: Optional[str] = None):
        """|coro|
        Unbans a user from the guild.

        Parameters
        ----------
        id : :class:`~pincer.utils.snowflake.Snowflake`
            The user ID
        reason : Optional[:class:`str`]
            The reason for unbanning the user |default| :data:`None`
        """
        await self._http.delete(
            f"guilds/{self.id}/bans/{id}",
            headers=remove_none({"X-Audit-Log-Reason": reason})
        )

    @overload
    async def edit(
        self,
        *,
        name: Optional[str] = None,
        region: Optional[str] = None,
        verification_level: Optional[int] = None,
        default_message_notifications: Optional[int] = None,
        explicit_content_filter: Optional[int] = None,
        afk_channel_id: Optional[Snowflake] = None,
        afk_timeout: Optional[int] = None,
        icon: Optional[str] = None,
        owner_id: Optional[Snowflake] = None,
        splash: Optional[str] = None,
        discovery_splash: Optional[str] = None,
        banner: Optional[str] = None,
        system_channel_id: Optional[Snowflake] = None,
        system_channel_flags: Optional[int] = None,
        rules_channel_id: Optional[Snowflake] = None,
        public_updates_channel_id: Optional[Snowflake] = None,
        preferred_locale: Optional[str] = None,
        features: Optional[List[GuildFeature]] = None,
        description: Optional[str] = None,
    ) -> Guild:
        """|coro|
        Modifies the guild

        Parameters
        ----------
        name : Optional[:class:`str`]
            Guild name |default| :data:`None`
        region : Optional[:class:`str`]
            Guild voice region ID |default| :data:`None`
        verification_level : Optional[:class:`int`]
            Verification level |default| :data:`None`
        default_message_notifications : Optional[:class:`int`]
            Default message notification level |default| :data:`None`
        explicit_content_filter : Optional[:class:`int`]
            Explicit content filter level |default| :data:`None`
        afk_channel_id : Optional[:class:`~pincer.utils.snowflake.Snowflake`]
            ID for AFK channel |default| :data:`None`
        afk_timeout : Optional[:class:`int`]
            AFK timeout in seconds |default| :data:`None`
        icon : Optional[:class:`str`]
            base64 1024x1024 png/jpeg/gif image for the guild icon
            (can be animated gif when the server
            has the `ANIMATED_ICON` feature) |default| :data:`None`
        owner_id : Optional[:class:`~pincer.utils.snowflake.Snowflake`]
            User ID to transfer guild ownership to (must be owner) |default| :data:`None`
        splash : Optional[:class:`str`]
            base64 16:9 png/jpeg image for the guild splash (when the
            server has the `INVITE_SPLASH` feature) |default| :data:`None`
        discovery_splash : Optional[:class:`str`]
            base64 16:9 png/jpeg image for the guild discovery splash
            (when the server has the `DISCOVERABLE` feature) |default| :data:`None`
        banner : Optional[:class:`str`]
            base64 16:9 png/jpeg image for the guild banner (when the
            server has the `BANNER` feature) |default| :data:`None`
        system_channel_id : Optional[:class:`~pincer.utils.snowflake.Snowflake`]
            The ID of the channel where guild notices such as welcome
            messages and boost events are posted |default| :data:`None`
        system_channel_flags : Optional[:class:`int`]
            System channel flags |default| :data:`None`
        rules_channel_id : Optional[:class:`~pincer.utils.snowflake.Snowflake`]
            The ID of the channel where Community guilds display rules
            and/or guidelines |default| :data:`None`
        public_updates_channel_id : Optional[:class:`~pincer.utils.snowflake.Snowflake`]
            The ID of the channel where admins and moderators of
            Community guilds receive notices from Discord |default| :data:`None`
        preferred_locale : Optional[:class:`str`]
            The preferred locale of a Community guild used in server
            discovery and notices from Discord; defaults to "en-US" |default| :data:`None`
        features : Optional[List[:class:`GuildFeature`]]
            Enabled guild features |default| :data:`None`
        description : Optional[:class:`str`]
            The description for the guild, if the guild is discoverable |default| :data:`None`

        Returns
        -------
        :class:`~pincer.objects.guild.Guild`
            The modified guild object.
        """
        ...

    async def edit(self, **kwargs) -> Guild:
        g = await self._http.patch(f"guilds/{self.id}", data=kwargs)
        return Guild.from_dict(construct_client_dict(self._client, g))

    async def preview(self) -> GuildPreview:
        """|coro|
        Previews the guild.

        Returns
        -------
        :class:`~pincer.objects.guild.guild.GuildPreview`
            The guild preview object.
        """
        data = await self._http.get(f"guilds/{self.id}/preview")
        return GuildPreview.from_dict(data)

    async def delete(self):
        """|coro|
        Deletes the guild. Returns `204 No Content` on success.
        """
        await self._http.delete(f"guilds/{self.id}")

    async def prune_count(
        self,
        days: Optional[int] = 7,
        include_roles: Optional[str] = None
    ) -> int:
        """|coro|
        Returns the number of members that
        would be removed in a prune operation.
        Requires the ``KICK_MEMBERS`` permission.

        Parameters
        ----------
        days : Optional[:class:`int`]
            Number of days to count prune for (1-30) |default| :data:`7`
        include_roles : Optional[:class:`str`]
            Comma-delimited array of Snowflakes;
            role(s) to include |default| :data:`None`

        Returns
        -------
        :class:`int`
            The number of members that would be removed.
        """
        return await self._http.get(
            f"guilds/{self.id}/prune?{days=}&{include_roles=!s}"
        )["pruned"]

    async def prune(
        self,
        days: Optional[int] = 7,
        compute_prune_days: Optional[bool] = True,
        include_roles: Optional[List[Snowflake]] = None,
        reason: Optional[str] = None
    ) -> int:
        """|coro|
        Prunes members from the guild. Requires the ``KICK_MEMBERS`` permission.

        Parameters

        Parameters
        ----------
        days : Optional[:class:`int`]
            Number of days to prune (1-30) |default| :data:`7`
        compute_prune_days : Optional[:class:`bool`]
            Whether ``pruned`` is returned, discouraged for large guilds
            |default| :data:`True`
        include_roles : Optional[List[:class:`~pincer.utils.snowflake.Snowflake`]]
            role(s) to include |default| :data:`None`
        reason : Optional[:class:`str`]
            Reason for the prune |default| :data:`None`

        Returns
        -------
        :class:`int`
            The number of members that were removed.
        """
        return await self._http.post(
            f"guilds/{self.id}/prune",
            data={
                "days": days,
                "compute_prune_days": compute_prune_days,
                "include_roles": include_roles
            },
            headers=remove_none({"X-Audit-Log-Reason": reason})
        )["pruned"]

    async def get_voice_regions(self) -> AsyncGenerator[VoiceRegion, None]:
        """|coro|
        Returns an async generator of voice regions.

        Yields
        -------
        AsyncGenerator[:class:`~pincer.objects.voice.VoiceRegion`, :data:`None`]
            An async generator of voice regions.
        """
        data = await self._http.get(f"guilds/{self.id}/regions")
        for voice_region_data in data:
            yield VoiceRegion.from_dict(construct_client_dict(self._client, voice_region_data))

    async def get_invites(self) -> AsyncGenerator[Invite, None]:
        """|coro|
        Returns an async generator of invites for the guild.
        Requires the ``MANAGE_GUILD`` permission.

        Yields
        -------
        AsyncGenerator[:class:`~pincer.objects.invite.Invite`, :data:`None`]
            An async generator of invites.
        """
        data = await self._http.get(f"guilds/{self.id}/invites")
        for invite_data in data:
            yield Invite.from_dict(construct_client_dict(self._client, invite_data))

    async def get_integrations(self) -> AsyncGenerator[Integration, None]:
        """|coro|
        Returns an async generator of integrations for the guild.
        Requires the ``MANAGE_GUILD`` permission.

        Yields
        -------
        AsyncGenerator[:class:`~pincer.objects.integration.Integration`, :data:`None`]
            An async generator of integrations.
        """
        data = await self._http.get(f"guilds/{self.id}/integrations")
        for integration_data in data:
            yield Integration.from_dict(construct_client_dict(self._client, integration_data))

    async def delete_integration(
        self,
        integration: Integration,
        reason: Optional[str] = None
    ):
        """|coro|
        Deletes an integration.
        Requires the ``MANAGE_GUILD`` permission.

        Parameters
        ----------
        integration : :class:`~pincer.objects.integration.Integration`
            The integration to delete.
        reason : Optional[:class:`str`]
            Reason for the deletion |default| :data:`None`
        """
        await self._http.delete(
            f"guilds/{self.id}/integrations/{integration.id}",
            headers=remove_none({"X-Audit-Log-Reason": reason})
        )

    async def get_widget_settings(self) -> GuildWidget:
        """|coro|
        Returns the guild widget settings.
        Requires the ``MANAGE_GUILD`` permission.

        Returns
        -------
        :class:`~pincer.objects.guild.widget.GuildWidget`
            The guild widget settings.
        """
        return GuildWidget.from_dict(
            construct_client_dict(
                self._client,
                await self._http.get(f"guilds/{self.id}/widget")
            )
        )

    async def modify_widget(
        self,
        reason: Optional[str] = None,
        **kwargs
    ) -> GuildWidget:
        """|coro|
        Modifies the guild widget for the guild.
        Requires the ``MANAGE_GUILD`` permission.

        Parameters
        ----------
        reason : Optional[:class:`str`]
            Reason for the modification |default| :data:`None`
        \\*\\*kwargs
            The widget settings to modify

        Returns
        -------
        :class:`~pincer.objects.guild.widget.GuildWidget`
            The updated GuildWidget object
        """
        data = await self._http.patch(
            f"guilds/{self.id}/widget",
            data=kwargs,
            headers=remove_none({"X-Audit-Log-Reason": reason})
        )
        return GuildWidget.from_dict(construct_client_dict(self._client, data))

    async def get_widget(self) -> Dict[str, JSONSerializable]:
        """|coro|
        Returns the widget for the guild
        """
        return await self._http.get(f"guilds/{self.id}/widget.json")

    @property
    async def vanity_url(self) -> Invite:
        """|coro|
        Returns the Vanity URL for the guild.
        Requires the ``MANAGE_GUILD`` permission.
        ``code`` will be null if a vanity URL has not been set.

        Returns
        -------
        :class:`~pincer.objects.guild.invite.Invite`
            The vanity url for the guild.
        """
        data = await self._http.get(f"guilds/{self.id}/vanity-url")
        return Invite.from_dict(construct_client_dict(self._client, data))

    async def get_widget_image(self, style: Optional[str] = "shield") -> str:  # TODO Replace str with ImageURL object
        """|coro|
        Returns a PNG image widget for the guild.
        Requires no permissions or authentication.

        Widget Style Options
        -------------------
        * [``shield``](https://discord.com/api/guilds/81384788765712384/widget.png?style=shield)
          shield style widget with Discord icon and guild members online count
        * [``banner1``](https://discord.com/api/guilds/81384788765712384/widget.png?style=banner1)
          large image with guild icon, name and online count.
          "POWERED BY DISCORD" as the footer of the widget
        * [``banner2``](https://discord.com/api/guilds/81384788765712384/widget.png?style=banner2)
          smaller widget style with guild icon, name and online count.
          Split on the right with Discord logo
        * [``banner3``](https://discord.com/api/guilds/81384788765712384/widget.png?style=banner3)
          large image with guild icon, name and online count.
          In the footer, Discord logo on the
          left and "Chat Now" on the right
        * [``banner4``](https://discord.com/api/guilds/81384788765712384/widget.png?style=banner4)
          large Discord logo at the top of the widget.
          Guild icon, name and online count in the middle portion
          of the widget and a "JOIN MY SERVER" button at the bottom

        Parameters
        ----------
        style : Optional[:class:`str`]
            Style of the widget image returned |default| :data:`"shield"`

        Returns
        -------
        :class:`str`
            A PNG image of the guild widget.
        """
        return await self._http.get(f"guilds/{self.id}/widget.png?{style=!s}")

    async def get_welcome_screen(self) -> WelcomeScreen:
        """Returns the welcome screen for the guild.

        Returns
        -------
        :class:`~pincer.objects.guild.welcome_screen.WelcomeScreen`
            The welcome screen for the guild.
        """
        data = await self._http.get(f"guilds/{self.id}/welcome-screen")
        return WelcomeScreen.from_dict(construct_client_dict(self._client, data))

    async def modify_welcome_screen(
        self,
        enabled: Optional[bool] = None,
        welcome_channels: Optional[List[WelcomeScreenChannel]] = None,
        description: Optional[str] = None,
        reason: Optional[str] = None
    ) -> WelcomeScreen:
        """|coro|
        Modifies the guild's Welcome Screen.
        Requires the ``MANAGE_GUILD`` permission.

        Parameters
        ----------
        enabled : Optional[:class:`bool`]
            Whether the welcome screen is enabled |default| :data:`None`
        welcome_channels : Optional[List[:class:`~pincer.objects.guild.welcome_screen.WelcomeScreenChannel`]]
            Channels linked in the welcome screen and
            their display options |default| :data:`None`
        description : Optional[:class:`str`]
            The server description to show
            in the welcome screen |default| :data:`None`
        reason : Optional[:class:`str`]
            Reason for the modification |default| :data:`None`

        Returns
        -------
        :class:`~pincer.objects.guild.welcome_screen.WelcomeScreen`
            The updated WelcomeScreen object
        """
        data = await self._http.patch(
            f"guilds/{self.id}/welcome-screen",
            data={
                "enabled": enabled,
                "welcome_channels": welcome_channels,
                "description": description
            },
            headers=remove_none({"X-Audit-Log-Reason": reason})
        )
        return WelcomeScreen.from_dict(construct_client_dict(self._client, data))

    async def modify_current_user_voice_state(
        self,
        channel_id: Snowflake,
        suppress: Optional[bool] = None,
        request_to_speak_timestamp: Optional[Timestamp] = None
    ):
        """|coro|
        Updates the current user's voice state.

        There are currently several caveats for this endpoint:
        * ``channel_id`` must currently point to a stage channel
        * current user must already have joined ``channel_id``
        * You must have the ``MUTE_MEMBERS`` permission to
          unsuppress yourself. You can always suppress yourself.
        * You must have the ``REQUEST_TO_SPEAK`` permission to request
          to speak. You can always clear your own request to speak.
        * You are able to set ``request_to_speak_timestamp`` to any
          present or future time.

        Parameters
        ----------
        channel_id : :class:`~pincer.utils.snowflake.Snowflake`
            The ID of the channel the user is currently in
        suppress : Optional[:class:`bool`]
            Toggles the user's suppress state |default| :data:`None`
        request_to_speak_timestamp : Optional[:class:`~pincer.utils.timestamp.Timestamp`]
            Sets the user's request to speak
        """
        await self._http.patch(
            f"guilds/{self.id}/voice-states/@me",
            data={
                "channel_id": channel_id,
                "suppress": suppress,
                "request_to_speak_timestamp": request_to_speak_timestamp
            }
        )

    async def modify_user_voice_state(
        self,
        user: User,
        channel_id: Snowflake,
        suppress: Optional[bool] = None
    ):
        """|coro|
        Updates another user's voice state.

        There are currently several caveats for this endpoint:
        * ``channel_id`` must currently point to a stage channel
        * User must already have joined ``channel_id``
        * You must have the ``MUTE_MEMBERS`` permission.
          (Since suppression is the only thing that is available currently.)
        * When unsuppressed, non-bot users will have their
          ``request_to_speak_timestamp`` set to the current time.
          Bot users will not.
        * When suppressed, the user will have their
          ``request_to_speak_timestamp`` removed.

        Parameters
        ----------
        user : :class:`~pincer.objects.guild.member.Member`
            The user to update
        channel_id : :class:`~pincer.utils.snowflake.Snowflake`
            The ID of the channel the user is currently in
        suppress : Optional[:class:`bool`]
            Toggles the user's suppress state |default| :data:`None`
        """
        await self._http.patch(
            f"guilds/{self.id}/voice-states/{user.id}",
            data={
                "channel_id": channel_id,
                "suppress": suppress
            }
        )

    async def get_audit_log(self) -> AuditLog:
        """|coro|
        Returns an audit log object for the guild.
        Requires the ``VIEW_AUDIT_LOG`` permission.

        Returns
        -------
        :class:`~pincer.objects.guild.audit_log.AuditLog`
            The audit log object for the guild.
        """
        return AuditLog.from_dict(
            construct_client_dict(
                self._client,
                await self._http.get(f"guilds/{self.id}/audit-logs")
            )
        )

    async def get_emojis(self) -> AsyncGenerator[Emoji, None]:
        """|coro|
        Returns an async generator of the emojis in the guild.

        Yields
        ------
        :class:`~pincer.objects.guild.emoji.Emoji`
            The emoji object.
        """
        data = await self._http.get(f"guilds/{self.id}/emojis")
        for emoji_data in data:
            yield Emoji.from_dict(
                construct_client_dict(self._client, emoji_data)
            )

    async def get_emoji(self, id: Snowflake) -> Emoji:
        """|coro|
        Returns an emoji object for the given ID.

        Parameters
        ----------
        id : :class:`~pincer.utils.snowflake.Snowflake`
            The ID of the emoji

        Returns
        -------
        :class:`~pincer.objects.guild.emoji.Emoji`
            The emoji object.
        """
        return Emoji.from_dict(
            construct_client_dict(
                self._client,
                await self._http.get(f"guilds/{self.id}/emojis/{id}")
            )
        )

    async def create_emoji(
        self,
        *,
        name: str,
        image: File,
        roles: List[Snowflake] = [],
        reason: Optional[str] = None
    ) -> Emoji:
        """|coro|
        Creates a new emoji for the guild.
        Requires the ``MANAGE_EMOJIS_AND_STICKERS`` permission.

        Emojis and animated emojis have a maximum file size of 256kb.
        Attempting to upload an emoji larger than this limit will fail.

        Parameters
        ----------
        name : :class:`str`
            Name of the emoji
        image : :class:`~pincer.objects.message.file.File`
            The File for the 128x128 emoji image data
        roles : List[:class:`~pincer.utils.snowflake.Snowflake`]
            Roles allowed to use this emoji |default| :data:`[]`
        reason : Optional[:class:`str`]
            The reason for creating the emoji |default| :data:`None`

        Returns
        -------
        :class:`~pincer.objects.guild.emoji.Emoji`
            The newly created emoji object.
        """
        data = await self._http.post(
            f"guilds/{self.id}/emojis",
            data={
                "name": name,
                "image": image.uri,
                "roles": roles
            },
            headers=remove_none({"X-Audit-Log-Reason": reason})
        )
        return Emoji.from_dict(
            construct_client_dict(self._client, data)
        )

    async def edit_emoji(
        self,
        id: Snowflake,
        *,
        name: Optional[str] = None,
        roles: Optional[List[Snowflake]] = None,
        reason: Optional[str] = None
    ) -> Emoji:
        """|coro|
        Modifies the given emoji.
        Requires the ``MANAGE_EMOJIS_AND_STICKERS`` permission.

        Parameters
        ----------
        id : :class:`~pincer.utils.snowflake.Snowflake`
            The ID of the emoji
        name : Optional[:class:`str`]
            Name of the emoji |default| :data:`None`
        roles : Optional[List[:class:`~pincer.utils.snowflake.Snowflake`]]
            Roles allowed to use this emoji |default| :data:`None`
        reason : Optional[:class:`str`]
            The reason for editing the emoji |default| :data:`None`

        Returns
        -------
        :class:`~pincer.objects.guild.emoji.Emoji`
            The modified emoji object.
        """
        data = await self._http.patch(
            f"guilds/{self.id}/emojis/{id}",
            data={
                "name": name,
                "roles": roles
            },
            headers=remove_none({"X-Audit-Log-Reason": reason})
        )
        return Emoji.from_dict(
            construct_client_dict(self._client, data)
        )

    async def delete_emoji(
        self,
        id: Snowflake,
        *,
        reason: Optional[str] = None
    ):
        """|coro|
        Deletes the given emoji.
        Requires the ``MANAGE_EMOJIS_AND_STICKERS`` permission.

        Parameters
        ----------
        id : :class:`~pincer.utils.snowflake.Snowflake`
            The ID of the emoji
        reason : Optional[:class:`str`]
            The reason for deleting the emoji |default| :data:`None`
        """
        await self._http.delete(
            f"guilds/{self.id}/emojis/{id}",
            headers=remove_none({"X-Audit-Log-Reason": reason})
        )

    async def get_templates(self) -> AsyncGenerator[GuildTemplate, None]:
        """|coro|
        Returns an async generator of the guild templates.

        Yields
        -------
        AsyncGenerator[:class:`~pincer.objects.guild.template.GuildTemplate`, :data:`None`]
            The guild template object.
        """
        data = await self._http.get(f"guilds/{self.id}/templates")
        for template_data in data:
            yield GuildTemplate.from_dict(
                construct_client_dict(self._client, template_data)
            )

    async def create_template(
        self,
        name: str,
        description: Optional[str] = None
    ) -> GuildTemplate:
        """|coro|
        Creates a new template for the guild.
        Requires the ``MANAGE_GUILD`` permission.

        Parameters
        ----------
        name : :class:`str`
            Name of the template (1-100 characters)
        description : Optional[:class:`str`]
            Description of the template
            (0-120 characters) |default| :data:`None`
        Returns
        -------
        :class:`~pincer.objects.guild.template.GuildTemplate`
            The newly created template object.
        """
        data = await self._http.post(
            f"guilds/{self.id}/templates",
            data={
                "name": name,
                "description": description
            }
        )
        return GuildTemplate.from_dict(
            construct_client_dict(self._client, data)
        )

    async def sync_template(
        self,
        template: GuildTemplate
    ) -> GuildTemplate:
        """|coro|
        Syncs the given template.
        Requires the ``MANAGE_GUILD`` permission.

        Parameters
        ----------
        template : :class:`~pincer.objects.guild.template.GuildTemplate`
            The template to sync

        Returns
        -------
        :class:`~pincer.objects.guild.template.GuildTemplate`
            The synced template object.
        """
        data = await self._http.put(
            f"guilds/{self.id}/templates/{template.code}"
        )
        return GuildTemplate.from_dict(
            construct_client_dict(self._client, data)
        )

    async def edit_template(
        self,
        template: GuildTemplate,
        *,
        name: Optional[str] = None,
        description: Optional[str] = None
    ) -> GuildTemplate:
        """|coro|
        Modifies the template's metadata.
        Requires the ``MANAGE_GUILD`` permission.

        Parameters
        ----------
        template : :class:`~pincer.objects.guild.template.GuildTemplate`
            The template to edit
        name : Optional[:class:`str`]
            Name of the template (1-100 characters)
            |default| :data:`None`
        description : Optional[:class:`str`]
            Description of the template (0-120 characters)
            |default| :data:`None`

        Returns
        -------
        :class:`~pincer.objects.guild.template.GuildTemplate`
            The edited template object.
        """
        data = await self._http.patch(
            f"guilds/{self.id}/templates/{template.code}",
            data={
                "name": name,
                "description": description
            }
        )
        return GuildTemplate.from_dict(
            construct_client_dict(self._client, data)
        )

    async def delete_template(
        self,
        template: GuildTemplate
    ) -> GuildTemplate:
        """|coro|
        Deletes the given template.
        Requires the ``MANAGE_GUILD`` permission.

        Parameters
        ----------
        template : :class:`~pincer.objects.guild.template.GuildTemplate`
            The template to delete
        
        Returns
        -------
        :class:`~pincer.objects.guild.template.GuildTemplate`
            The deleted template object.
        """
        data = await self._http.delete(
            f"guilds/{self.id}/templates/{template.code}"
        )
        return GuildTemplate.from_dict(
            construct_client_dict(self._client, data)
        )

    async def get_webhooks(self) -> AsyncGenerator[Webhook, None]:
        """|coro|
        Returns an async generator of the guild webhooks.

        Yields
        -------
        AsyncGenerator[:class:`~pincer.objects.guild.webhook.Webhook`, None]
            The guild webhook object.
        """
        data = await self._http.get(f"guilds/{self.id}/webhooks")
        for webhook_data in data:
            yield Webhook.from_dict(
                construct_client_dict(self._client, webhook_data)
            )

    @classmethod
    def from_dict(cls, data) -> Guild:
        """
        Parameters
        ----------
        data : :class:`Dict`
            Guild data received from the discord API.
        Returns
        -------
        :class:`~pincer.objects.guild.guild.Guild`
            The new guild object.
        Raises
        :class:`~pincer.exceptions.UnavailableGuildError`
            The guild is unavailable due to a discord outage.
        """
        if data.get("unavailable", False):
            raise UnavailableGuildError(
                f"Guild \"{data['id']}\" is unavailable due to a discord"
                " outage."
            )

        return super().from_dict(data)


@dataclass(repr=False)
class UnavailableGuild(APIObject):
    id: Snowflake
    unavailable: bool = True
