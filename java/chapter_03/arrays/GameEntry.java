package chapter_03.arrays;

import lombok.Getter;
import lombok.RequiredArgsConstructor;
import lombok.ToString;

@Getter
@RequiredArgsConstructor
@ToString
public class GameEntry {

    private final String name;

    private final int score;
}
