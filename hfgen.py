import sys
import os


class Author():
	def __init__(self, line):
		self.line = line
		self.parse_line()

	def parse_line(self):
		tokens = self.line.split(' (')[0].split()
		if tokens[len(tokens) - 1].isdigit():
			self.last_name = tokens[len(tokens) - 2]
			self.first_name = ' '.join(tokens[:len(tokens) - 2])
		else:
			self.last_name = tokens[len(tokens) - 1]
			self.first_name = ' '.join(tokens[:len(tokens) - 1])
		self.name = self.last_name + ', ' + self.first_name
		self.total = int(self.line.split('total=')[1].split(')')[0])
		self.count_per_year = self.line.split('): ')[1].rstrip('\n').rstrip(',').replace('0', ' ').split(',')

	def get_name(self):
		return self.name

	def get_total(self):
		return self.total

	def get_count_per_year(self):
		return self.count_per_year


class LeaderBoard():
	def __init__(self, fin_path, first_year, last_year):
		self.fin_path = fin_path
		self.first_year = first_year
		self.last_year = last_year
		self.get_authors()

	def get_authors(self):
		self.authors = []
		with open(self.fin_path, 'r') as fin:
			cur_total = 0
			prev_total = 0
			temp = []
			for line in fin:
				a = Author(line)
				cur_total = a.get_total()
				if cur_total != prev_total and prev_total != 0:
					for t in sorted(temp, key=lambda x: x.get_name()):
						self.authors.append(t)
					temp = []
				temp.append(a)
				prev_total = cur_total

	def html_leader_board(self, cutoff=8):
		buffer = ''
		with open('header.html', 'r') as fin:
			for line in fin:
				buffer += line
		buffer += '<table>\n'
		buffer += '  <tr>\n'
		buffer += '    <th rowspan="2">Count</th>\n'
		buffer += '    <th rowspan="2">Name</th>\n'
		first_decade = self.first_year / 10
		last_decade = self.last_year / 10
		current_decade = first_decade
		year_labels = []
		while current_decade <= last_decade:
			if current_decade == first_decade:
				buffer += '    <th colspan="%d">%d0\'s</th>\n'%(10-self.first_year%10, current_decade)
				year_labels += range(self.first_year%10, 10)
			elif current_decade == last_decade:
				buffer += '    <th colspan="%d">%d0\'s</th>\n'%(self.last_year%10+1, current_decade)
				year_labels += range(0, self.last_year%10+1)
			else:
				buffer += '    <th colspan="10">%d0\'s</th>\n'%(current_decade)
				year_labels += range(0, 10)
			current_decade += 1
		buffer += '  </tr>\n'
		buffer += '  <tr>\n'
		for i in year_labels:
			if i % 10 == 9:
				buffer += '    <th class="right-bottom-border">' + str(i) + '</th>\n'
			else:
				buffer += '    <th class="bottom-border">' + str(i) + '</th>\n'
		buffer += '  </tr>\n'
		cur_total = 0
		prev_total = 0
		for a in self.authors:
			cur_total = a.get_total()
			if cur_total < cutoff:
				break
			else:
				#if cur_total != prev_total and prev_total != 0:
				#	buffer += '\n'
				#buffer += ('%d\t' % (cur_total)).expandtabs(6)
				#buffer += ('%s\t' % (a.get_name())).expandtabs(30)
				#buffer += ''.join(a.get_count_per_year())
				#buffer += '\n'
				if cur_total != prev_total and prev_total != 0:
					buffer += '  <tr class="top-border">\n'
				else:
					buffer += '  <tr>\n'
				buffer += '    <td class="right-border">' + str(cur_total) + '</td>\n'
				buffer += '    <td class="right-border">' + a.get_name() + '</td>\n'
				year = 1995
				for i, c in enumerate(a.get_count_per_year()):
					if (year + i) % 10 == 9:
						buffer += '    <td class="right-border-1px">' + c + '</td>\n'
					else:
						buffer += '    <td>' + c + '</td>\n'
				buffer += '  </tr>\n'
			prev_total = cur_total
		buffer += '</table>\n</body>\n</html>'
		return buffer


def usage():
	print '[Usage]'


def main():
	if len(sys.argv) < 2:
		usage()
	first_year = 1995
	last_year = int(sys.argv[1])
	with open('hpca_hof_%d.html'%last_year, 'w') as fout:
		fout.write(LeaderBoard('data/%d.in'%last_year, first_year, last_year).html_leader_board())


if __name__ == '__main__':
	main()