public class Bid {
    private long price;
    private Person bidder;

    public Bid(Person bidder, long price) {
        if(bidder == null){
            throw new NullPointerException();
        }
        if(price <= 0){
            throw new IllegalArgumentException();
        }
        this.price = price;
        this.bidder = bidder;
    }

    public long getPrice() {
        return price;
    }

    public Person getBidder() {
        return bidder;
    }

    @Override
    public String toString() {
        return price + " EUR by " + bidder.toString();
    }
}
