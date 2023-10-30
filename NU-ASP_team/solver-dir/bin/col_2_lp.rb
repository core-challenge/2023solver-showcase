# coding: utf-8
# args .col
if ARGV.length != 1 then
    puts "Segment Error"
    exit
end

file = File.open(ARGV[0], "r")
file.gets()
while !($_.nil?) # nil mean EOF
  if (tmp = $_.match(/^p\s+(\d+)\s+(\d+)/)) != nil then
    ver_num = tmp[1].to_i
    puts "n(#{ver_num})."
    puts "e(#{tmp[2]})."
    for i in 1 .. ver_num do
      puts "node(#{i})."
    end
  elsif (tmp = $_.match(/^e\s+(\d+)\s+(\d+)/)) != nil then
      puts "edge(#{tmp[1]}, #{tmp[2]})."
  end
  file.gets()
end

file.close
