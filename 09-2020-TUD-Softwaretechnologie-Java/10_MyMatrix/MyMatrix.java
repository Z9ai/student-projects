import java.util.*;

public class MyMatrix<T> implements Matrix<T>{
    private Map<MatrixIndex,T> matrixEntries = new HashMap<>();

    @Override
    public int getRowCount() {
        int counter = 0;
        for(MatrixIndex index : matrixEntries.keySet()){
            if (index.getRow()+1 > counter  &&  matrixEntries.get(index) != null){
                counter = index.getRow()+1;
            }
        }
        return counter;
    }

    @Override
    public int getColumnCount() {
        int counter = 0;
        for(MatrixIndex index : matrixEntries.keySet()){
            if (index.getColumn()+1 > counter  &&  matrixEntries.get(index) != null){
                counter = index.getColumn()+1;
            }
        }
        return counter;
    }

    @Override
    public int getObjectCount() {
        int counter = 0;
        for(MatrixIndex index : matrixEntries.keySet()){
            if (matrixEntries.get(index) != null){
                counter = counter +1;
            }
        }
        return counter;
    }

    @Override
    public int getDistinctObjectCount() {

        Set<T> distinctObjects = new HashSet<>();
        for(MatrixIndex index : matrixEntries.keySet()){
            if (matrixEntries.get(index) != null){
                distinctObjects.add(matrixEntries.get(index));
            }
        }
        return distinctObjects.size();
    }

    @Override
    public Iterator<T> iterator() {
        return new DepthFirstIterator<T>();
    }

    @Override
    public T get(int row, int column) {
        T value = null;
        if(row<0 || column<0){
            throw new IllegalArgumentException();
        }
        if(row >=(this.getRowCount())|| column >= (this.getColumnCount())){

            throw new IllegalArgumentException();
        }
        for(MatrixIndex index : matrixEntries.keySet()){
            if (index.getColumn()==column && index.getRow() == row) {
                value =  matrixEntries.get(index);
            }
        }
        return value;
    }

    @Override
    public T put(int row, int column, T value) {
        if(row<0 || column<0){
            throw new IllegalArgumentException();
        }
        for(MatrixIndex index : matrixEntries.keySet()){
            if (index.getColumn()==column && index.getRow() == row) {
                T valueOld = matrixEntries.get(index);
                matrixEntries.put(index, value);
                return valueOld;
            }
        }
        matrixEntries.put(new MatrixIndex(row, column), value);
        return null;
    }

    @Override
    public boolean contains(T value) {
        if(matrixEntries == null){
            throw new NullPointerException();
        }
        if (matrixEntries.containsValue(value)){
            return true;
        }
        return false;
    }






    


    class DepthFirstIterator<T> implements Iterator<T>{

        public DepthFirstIterator(){
        }

        @Override
        public boolean hasNext() {
            if(matrixEntries.isEmpty()){
                return false;
            }
            return true;
        }

        @Override
        public T next() {
            T value = null;
            Set<Integer> columnExisting = new HashSet<>();
            for (MatrixIndex index : matrixEntries.keySet()){
                if(matrixEntries.get(index) != null){
                    columnExisting.add(index.getColumn());
                }
            }
            int minColumn = Collections.min(columnExisting);
            Set<Integer> rowsInMinColumn = new HashSet<>();
            for (MatrixIndex index : matrixEntries.keySet()){
                if (index.getColumn() == minColumn){
                    rowsInMinColumn.add(index.getRow());
                }
            }
            int minRow = Collections.min(rowsInMinColumn);
            for(MatrixIndex index : matrixEntries.keySet()){
                if(index.getColumn() == minColumn && index.getRow() == minRow){
                    MatrixIndex key = index;
                    value = (T) matrixEntries.get(key);
                    matrixEntries.remove(key);
                    return value;
                }
            }
            return value;
        }

        @Override
        public void remove() {
            throw new UnsupportedOperationException();
        }
    }
}
