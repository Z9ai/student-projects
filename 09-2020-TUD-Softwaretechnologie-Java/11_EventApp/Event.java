public class Event implements Comparable<Event>{
    private String title;
    private EventCategory category;

    public Event(String title, EventCategory category){
        if (title == "") {
            throw new IllegalArgumentException();
        }
        if (category == null|| title == null) {
            throw new NullPointerException();
        }
        this.title = title;
        this.category = category;
    }

    @Override
    public int compareTo(Event o) {
        if (title.compareTo(o.title) == 0){
            return category.compareTo(o.category);
        }
        return title.compareTo(o.title);
    }

    public String getTitle() {
        return title;
    }

    public EventCategory getCategory() {
        return category;
    }
}
