const std = @import("std");
const stdout = std.io.getStdOut().writer();

pub fn main () !void {
    var file = try std.fs.cwd().openFile("inputs/input_02.txt", .{});
    defer file.close();

    const reader = file.reader();
    var result = try part_1(reader);
    try stdout.print("part 1 safe reports: {}\n", .{result});

    try file.seekTo(0);

    result = try part_2(reader);
    try stdout.print("part 2 safe reports: {}\n", .{result});
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
    var safe_reports: u16 = 0;
    var line_buffer: [128]u8 = undefined;

    while (try reader.readUntilDelimiterOrEof( &line_buffer, '\n')) |line| {
        const trimmed_line = std.mem.trimRight(u8, line, " \n\t\r");
        if (try is_line_safe(trimmed_line)) safe_reports += 1;
    }

    return safe_reports;
}

fn is_line_safe(line: []const u8) !bool {
    const allocator = std.heap.page_allocator;

    var tokenizer = std.mem.tokenizeSequence(u8, line, " ");
    var levels = std.ArrayList(i64).init(allocator);
    defer levels.deinit();

    // Parse levels
    while (tokenizer.next()) |token| {
        try levels.append(try std.fmt.parseInt(i64, token, 10));
    }

    const levels_slice = levels.items;

    if (is_sequence_safe(levels_slice)) return true;

    // brute force removing each level
    for (0..levels_slice.len) |j| {
        var temp_levels = std.ArrayList(i64).init(allocator);
        defer temp_levels.deinit();

        for (0..levels_slice.len) |k| {
            if (k != j) {
                try temp_levels.append(levels_slice[k]);
            }
        }

        if (is_sequence_safe(temp_levels.items)) return true;
    }

    return false;
}

fn is_sequence_safe(sequence: []const i64) bool {
    if (sequence.len < 2) return true;
    const increasing = sequence[1] > sequence[0];
    var previous = sequence[0];

    for(sequence[1..]) |current| {
        const diff = @abs(current - previous);
        if (diff > 3 or (increasing and current <= previous) or !increasing and current >= previous) {
            return false;
        }
        previous = current;
    }
    return true;
}