from dataclasses import dataclass

from ffxiahbot.auction.worker import Worker
from ffxiahbot.logutils import capture, logger
from ffxiahbot.tables.auctionhouse import AuctionHouse


@dataclass(frozen=True)
class Cleaner(Worker):
    """
    Auction House cleaner.
    """

    def clear(self, seller: int | None = None) -> None:
        """
        Clear out auction house.

        Args:
            seller: The seller to clear out (if None, all rows are cleared).
        """
        # clear rows
        if seller is None:
            # perform query
            with self.scoped_session() as session:
                n = session.query(AuctionHouse).delete()
                logger.info("%d rows dropped", n)

        # clear rows of seller
        else:
            # validate seller
            with capture(fail=self.fail):
                if not isinstance(seller, int) or not seller >= 0:
                    raise RuntimeError("invalid seller: %s", seller)

                # perform query
                with self.scoped_session() as session:
                    n = (
                        session.query(AuctionHouse)
                        .filter(
                            AuctionHouse.seller == seller,
                        )
                        .delete()
                    )
                    logger.info("%d rows dropped", n)
