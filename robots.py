class Robots:

    def __init__(self):
        self.sitemaps = set()
        self.entries = []

    def __str__(self):
        entries = []
        for sitemap in sorted(self.sitemaps):
            entries.append('Sitemap: '+ sitemap)
        for entry in self.entries:
            entries.append(str(entry))
        return '\n\n'.join(entries)

    def to_dict(self):
        ''' return json-serializable dict representation of Robots '''
        d = {}
        if self.entries:
            d['entries'] = [x.to_dict() for x in self.entries]
        if self.sitemaps:
            d['sitemaps'] = sorted(self.sitemaps)
        return d

    def parse(self, lines):
        ''' parse lines of robots.txt file '''
        entry = Entry()
        for line in lines:
            # valid lines should have the colon before this point
            if ':' not in line[:16]:
                continue
            key, value = line.split(':', 1)
            key = key.strip().lower()
            value = value.strip()
            if key in ('allow', 'disallow'):
                entry.rules.add((key, value))
            elif key == 'user-agent':
                if entry.rules:
                    # Any user-agent after any rules starts a new entry
                    self.entries.append(entry)
                    entry = Entry()
                entry.user_agents.add(value)
            elif key == 'crawl-delay':
                try:
                    entry.crawl_delay = int(value)
                except ValueError:
                    pass
            elif key == 'sitemap':
                self.sitemaps.add(value)
        if entry.rules:
            self.entries.append(entry)


class Entry:

    def __init__(self):
        self.crawl_delay = None
        self.rules = set()
        self.user_agents = set()

    def __str__(self):
        lines = []
        for user_agent in sorted(self.user_agents):
            lines.append('User-agent: ' + user_agent)
        for rule, path in sorted(self.rules):
            lines.append('{}: {}'.format(rule.capitalize(), path))
        if self.crawl_delay is not None:
            lines.append('Crawl-delay: {}'.format(self.crawl_delay))
        return '\n'.join(lines)

    def to_dict(self):
        ''' return json-serializable dict representation of Entry '''
        d = {
            'rules': sorted(self.rules),
            'user_agents': sorted(self.user_agents),
        }
        if self.crawl_delay is not None:
            d['crawl_delay'] = self.crawl_delay
        return d
