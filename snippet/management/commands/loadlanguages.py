from operator import itemgetter
from django.core.management import BaseCommand, CommandError
from django.db import IntegrityError
from snippet.models import Language


REQUIRED = (
    # language_code, slug, name
    ('autodetect', 'autodetect', 'Auto-detect'),
    ('text', 'text', 'Plain text'),
)


ALL = (
    ('lua', 'lua', 'Lua'),
    ('perl6', 'perl6', 'Perl 6'),
    ('perl', 'perl', 'Perl'),
    ('python', 'python', 'Python'),
    ('pytb', 'pytb', 'Python traceback'),
    ('python3', 'python3', 'Python 3'),
    ('py3tb', 'py3tb', 'Python 3 traceback'),
    ('pycon', 'pycon', 'Python console'),
    ('ruby', 'ruby', 'Ruby'),
    ('irb', 'irb', 'Ruby console'),
    ('tcl', 'tcl', 'Tcl'),
    ('ada', 'ada', 'Ada'),
    ('c', 'c', 'C'),
    ('cobol', 'cobol', 'Cobol'),
    ('cpp', 'cpp', 'C++'),
    ('cuda', '', 'CUDA'),
    ('d', '', 'D'),
    ('delphi', '', 'Delphi'),
    ('fortran', '', 'Fortran'),
    ('glsl', '', 'GLSL'),
    ('go', '', 'Go'),
    ('obj-c', '', 'Objective-C'),
    ('prolog', '', 'Prolog'),
    ('vala', '', 'Vala'),
    ('csharp', '', 'C#'),
    ('aspx-cs', '', 'C# with ASP.NET'),
    ('fsharp', '', 'F#'),
    ('vbnet', '', 'Visual Basic.NET'),
    ('aspx-vb', '', 'Visual Basic.NET with ASP.NET'),
    ('lisp', '', 'Common Lisp'),
    ('erlang', '', 'Erlang'),
    ('erl', '', 'Erlang shell'),
    ('haskell', '', 'Haskell'),
    ('scheme', '', 'Scheme'),
    ('scala', '', 'Scala'),
    ('matlab', '', 'Matlab'),
    ('awk', '', 'AWK'),
    ('brainfuck', '', 'Brainfuck'),
    ('gnuplot', '', 'Gnuplot'),
    ('postscript', '', 'PostScript'),
    ('puppet', '', 'Puppet'),
    ('spec', 'rpmspec', 'RPM spec'),
    ('smalltalk', '', 'Smalltalk'),
    ('mysql', '', 'MySQL'),
    ('postgres', '', 'PostgreSQL'),
    ('plpgsql', '', 'Pl/pgSQL'),
    ('psql', '', 'PostgreSQL console'),
    ('sql', '', 'SQL'),
    ('sqlite', '', 'SQLite'),
    ('apacheconf', '', 'Apache configuration'),
    ('bbcode', '', 'BBCode'),
    ('cmake', '', 'CMake'),
    ('diff', '', 'Diff'),
    ('http', '', 'HTTP'),
    ('ini', '', 'Ini'),
    ('make', '', 'Makefile'),
    ('lighttpd', '', 'Lighttpd configuration'),
    ('nginx', '', 'Nginx configuration'),
    ('tex', '', 'TeX and LaTeX'),
    ('yaml', '', 'YAML'),
    ('as', '', 'ActionScript'),
    ('as3', '', 'ActionScript 3'),
    ('coffeescript', '', 'CoffeeScript'),
    ('css', '', 'CSS'),
    ('dtd', '', 'DTD'),
    ('haml', '', 'Haml'),
    ('html', '', 'HTML'),
    ('js', '', 'JavaScript'),
    ('php', '', 'PHP'),
    ('qml', '', 'QML'),
    ('scaml', '', 'Scaml'),
    ('ts', '', 'TypeScript'),
    ('xml', '', 'XML'),
    ('bash', '', 'Bash'),
    ('console', '', 'Bash session'),
    ('bat', '', 'Bat'),
    ('powershell', '', 'PowerShell'),
    ('elixir', 'ex', 'Elixir'),
    ('verilog', '', 'Verilog'),
    ('md', '', 'Markdown'),
    ('nix', '', 'Nix'),
)


class Command(BaseCommand):
    help = 'Loads a set of languages to database'

    def add_arguments(self, parser):
        parser.add_argument('language_set', choices=['all', 'required'])

    def handle(self, *args, **options):
        langs = ()

        if options['language_set'] == 'required':
            langs = REQUIRED
        else:
            langs = sorted((REQUIRED + ALL)[1:], key=itemgetter(2))
            langs = [REQUIRED[0],] + langs

        for lang in langs:
            slug = lang[1] if len(lang[1]) else lang[0]

            try:
                Language.objects.create(language_code=lang[0], slug=slug, name=lang[2])
                print(lang[2])
            except IntegrityError:
                continue

        self.stdout.write("Done")
