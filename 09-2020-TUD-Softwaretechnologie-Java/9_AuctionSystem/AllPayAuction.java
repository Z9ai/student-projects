public class AllPayAuction extends Auction{
    @Override
    public String generateItemString(Item item) {
        if(item.getAllBids().isEmpty()){
            return item.toString() + "\nNo bids placed";
        }
        String string = item.toString() + "\nHighest bid: "+ item.getHighestBid().toString()+"\nAll bids:" ;
        for(Bid bid: item.getAllBids()){
            string = string + "\n"+bid.toString();
        }
        return string;
    }
}
