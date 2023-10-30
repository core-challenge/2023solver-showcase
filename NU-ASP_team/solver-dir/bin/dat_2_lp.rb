# args .col
if ARGV.length != 1 then
    puts "Segment Error"
    exit
end

file = File.open(ARGV[0], "r")
lines = file.read().split("\n")
file.close

puts "k(#{lines[0].split(" ").length - 1})."  # output independent set size

lines.each do | line |
    line = line.split(" ")
    if line[0] == "s" then
        for i in 1 .. line.length - 1
            puts "start(#{line[i]})." # output start/1
        end
    elsif line[0] == "t" then
        for i in 1 .. line.length - 1
            puts "goal(#{line[i]})." # output goal/1
        end
    end
end

