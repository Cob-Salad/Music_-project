"""create database of songs

Revision ID: 6dca147e35b2
Revises: 169b1aff0a2c
Create Date: 2024-05-14 08:21:59.369534

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6dca147e35b2'
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table("playlist",
                    sa.Column("playlist_id", sa.INTEGER, primary_key=True),
                    sa.Column("playlist_name", sa.Text),
                    sa.Column("playlist_length", sa.INTEGER),
                )
    op.create_table("song", 
                    sa.Column("song_id", sa.Text, primary_key=True),
                    sa.Column("song_name", sa.Text),
                    sa.Column("artist_name", sa.Text),
                    sa.Column("album_name", sa.Text),
                )
    op.create_table("playlistsonglink", 
                    sa.Column("song_id", sa.Text, nullable=False),
                    sa.Column("playlist_id", sa.INTEGER, nullable=False),
                    sa.ForeignKeyConstraint(["song_id"], ["song.song_id"]),
                    sa.ForeignKeyConstraint(["playlist_id"], ["playlist.playlist_id"]),
                    sa.PrimaryKeyConstraint("song_id", "playlist_id", name="playlist_song_id")
                )


def downgrade() -> None:
    op.drop_table("playlistsonglink")
    op.drop_table("playlist")
    op.drop_table("song")