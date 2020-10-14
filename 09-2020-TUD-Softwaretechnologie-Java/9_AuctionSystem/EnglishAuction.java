public class EnglishAuction extends Auction {

    @Override
    public String generateItemString(Item item) {
        if(item.getAllBids().isEmpty()){
            return item.toString() + "\nNo bids placed";
        }
        return item.toString() + "\nHighest bid: " + item.getHighestBid().toString();
    }
}
