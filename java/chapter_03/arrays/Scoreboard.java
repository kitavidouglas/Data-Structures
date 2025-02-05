package chapter_03.arrays;

public class Scoreboard {

    private int numEntries = 0;

    private GameEntry[] board;

    public Scoreboard(int capacity) {
        board = new GameEntry[capacity];
    }

    public void add(GameEntry entry) {
        int newScore = entry.getScore();
        // is the new entry (e) a high score?
        if (numEntries < board.length || newScore > board[numEntries - 1].getScore()) {
            if (numEntries < board.length) {
                numEntries++;
            }
            int pointer = numEntries - 1;
            while (pointer > 0 && board[pointer - 1].getScore() < newScore) {
                board[pointer] = board[pointer - 1]; // shifting
                pointer--;
            }
            board[pointer] = entry; // add the new high score
        }
    }

    public GameEntry remove(int index) {
        if (index < 0 || index >= numEntries) {
            throw new IndexOutOfBoundsException("Invalid index: " + index);
        }
        GameEntry temp = board[index]; // to be removed
        for (int pointer = index; pointer < numEntries - 1; pointer++) {
            board[pointer] = board[pointer + 1]; // shifting
        }
        board[numEntries - 1] = null; // null out old last score
        numEntries--;
        return temp;
    }

    public static void main(String[] args) {
        Scoreboard scoreboard = new Scoreboard(5);
        scoreboard.add(new GameEntry("1st", 100));
        scoreboard.add(new GameEntry("2d", 120));
        scoreboard.add(new GameEntry("3rd", 90));
        scoreboard.add(new GameEntry("4th", 110));
        scoreboard.add(new GameEntry("5th", 80));
        scoreboard.add(new GameEntry("6th", 90));
        scoreboard.add(new GameEntry("8th", 80));
        scoreboard.add(new GameEntry("9th", 130));
        scoreboard.add(new GameEntry("10th", 110));

        scoreboard.remove(3);
    }
}
