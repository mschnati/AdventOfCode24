const std = @import("std");
const stdout = std.io.getStdOut().writer();

pub fn main () !void {
    var file = try std.fs.cwd().openFile("inputs/input_02.txt", .{});
    defer file.close();
    
    const reader = file.reader();
    const result = try part_1(reader);
    try stdout.print("part 1 safe reports: {}\n", .{result});
}

fn part_1 (reader: anytype) !u16 {
    var safe_reports: u16 = 0;
    var line_buffer: [128]u8 = undefined;
 
    // iterate lines
    while (try reader.readUntilDelimiterOrEof( &line_buffer, '\n')) |line| {
        var safe: bool = true;
        const trimmed_line = std.mem.trimRight(u8, line, " \n\t\r"); 
        var tokenizer = std.mem.tokenizeSequence(u8, trimmed_line, " ");

        var previous = try std.fmt.parseInt(i64, tokenizer.next().?, 10);
        var current = try std.fmt.parseInt(i64, tokenizer.next().?, 10);
        
        const increasing: bool = current > previous;
        if (!is_safe(previous, current, increasing)) continue;
        previous = current;

        // iterate values in line
        while (tokenizer.next()) |token| {
            current = try std.fmt.parseInt(i64, token, 10);
            if (!is_safe(previous, current, increasing)) {
                safe = false;
                break;
            }
            previous = current;
        }
        if (safe) safe_reports += 1;
    }

    return safe_reports;
}

fn is_safe(previous: i64, current: i64, increasing: bool) bool {
    const diff = current - previous;
    if (diff == 0 or @abs(diff) > 3) return false;
    return (increasing and diff > 0) or (!increasing and diff < 0); 
}

fn part_2 (reader: anytype) !u16 {
    _ = reader;
}