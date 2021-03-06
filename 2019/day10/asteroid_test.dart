import "package:test/test.dart";
import "asteroid.dart";

void main() {
  test("Simple", testSimple);
  test("Bigger", testBigger);
  test("Vaporization", testVaporizationSimple);
  test("Vaporization2", testVaporizationBigger);
}

void testSimple() {
  List<String> input = [".#..#", ".....", "#####", "....#", "...##"];
  List<Point> points = parsePoints(input);
  expect(points.length, 10);
  Point greatestPoint = findGreatestPoint(points);
  expect(greatestPoint, Point(3, 4));

  Point origin = new Point(1, 1);
  Point up = new Point(1, 0);
  expect(origin.getAngleInDegrees(up), 0);
  expect(origin.getDistance(up), 1);
  Point right = new Point(2, 1);
  expect(origin.getAngleInDegrees(right), 90);
  expect(origin.getDistance(right), 1);
  Point down = new Point(1, 2);
  expect(origin.getAngleInDegrees(down), 180);
  Point left = new Point(0, 1);
  expect(origin.getAngleInDegrees(left), 270);
}

void testBigger() {
  List<String> input = [
    "......#.#.",
    "#..#.#....",
    "..#######.",
    ".#.#.###..",
    ".#..#.....",
    "..#....#.#",
    "#..#....#.",
    ".##.#..###",
    "##...#..#.",
    ".#....####"
  ];
  List<Point> points = parsePoints(input);
  expect(points.length, 40);
  Point greatestPoint = findGreatestPoint(points);
  expect(greatestPoint.x, 5);
  expect(greatestPoint.y, 8);
}

void testVaporizationSimple() {
  List<String> input = [
    ".#....#####...#..",
    "##...##.#####..##",
    "##...#...#.#####.",
    "..#.....#...###..",
    "..#.#.....#....##"
  ];
  List<Point> points = parsePoints(input);
  Point greatestPoint = findGreatestPoint(points);
  expect(greatestPoint, Point(8, 3));
  List<Point> vaporizationOrder = getVaporizationOrder(points, greatestPoint);
  expect(points.length - 1, vaporizationOrder.length);

  expect(vaporizationOrder[0], Point(8, 1));
  expect(vaporizationOrder[1], Point(9, 0));
  expect(vaporizationOrder[2], Point(9, 1));
}

void testVaporizationBigger() {
  List<String> input = [
    ".#..##.###...#######",
    "##.############..##.",
    ".#.######.########.#",
    ".###.#######.####.#.",
    "#####.##.#.##.###.##",
    "..#####..#.#########",
    "####################",
    "#.####....###.#.#.##",
    "##.#################",
    "#####.##.###..####..",
    "..######..##.#######",
    "####.##.####...##..#",
    ".#####..#.######.###",
    "##...#.##########...",
    "#.##########.#######",
    ".####.#.###.###.#.##",
    "....##.##.###..#####",
    ".#.#.###########.###",
    "#.#.#.#####.####.###",
    "###.##.####.##.#..##"
  ];

  List<Point> points = parsePoints(input);
  Point greatestPoint = findGreatestPoint(points);
  expect(greatestPoint, Point(11, 13));
  List<Point> order = getVaporizationOrder(points, greatestPoint);
  expect(points.length - 1, order.length);

  expect(order[0], Point(11, 12));
  expect(order[1], Point(12, 1));
  expect(order[199], Point(8, 2));
}
