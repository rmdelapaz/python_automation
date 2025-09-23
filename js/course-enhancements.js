/* Prism.js 1.29.0 - Minimal Python Syntax Highlighting */

var _self = (typeof window !== 'undefined')
	? window
	: (
		(typeof WorkerGlobalScope !== 'undefined' && self instanceof WorkerGlobalScope)
		? self
		: {}
	);

var Prism = (function (_self) {
	var lang = /(?:^|\s)lang(?:uage)?-([\w-]+)(?=\s|$)/i;
	var uniqueId = 0;

	var _ = {
		util: {
			encode: function encode(tokens) {
				if (tokens instanceof Token) {
					return new Token(tokens.type, encode(tokens.content), tokens.alias);
				} else if (Array.isArray(tokens)) {
					return tokens.map(encode);
				} else {
					return tokens.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/\u00a0/g, ' ');
				}
			},

			type: function (o) {
				return Object.prototype.toString.call(o).slice(8, -1);
			},

			clone: function deepClone(o) {
				var clone, id;
				var type = _.util.type(o);

				switch (type) {
					case 'Object':
						id = o.$$id;
						if (id) {
							return cached[id];
						}
						clone = {};
						o.$$id = id = ++uniqueId;
						cached[id] = clone;

						for (var key in o) {
							if (o.hasOwnProperty(key)) {
								clone[key] = deepClone(o[key]);
							}
						}

						delete o.$$id;

						return clone;

					case 'Array':
						id = o.$$id;
						if (id) {
							return cached[id];
						}
						clone = [];
						o.$$id = id = ++uniqueId;
						cached[id] = clone;

						o.forEach(function (v, i) {
							clone[i] = deepClone(v);
						});

						delete o.$$id;

						return clone;

					default:
						return o;
				}
			}
		},

		languages: {
			python: {
				'comment': {
					pattern: /(^|[^\\])#.*/,
					lookbehind: true
				},
				'string-interpolation': {
					pattern: /(?:f|rf|fr)(?:("""|''')[\s\S]*?\1|("|')(?:\\.|(?!\2)[^\\\r\n])*\2)/i,
					greedy: true,
					inside: {
						'interpolation': {
							pattern: /((?:^|[^{])(?:\{\{)*)\{(?!\{)(?:[^{}]|\{(?!\{)(?:[^{}]|\{(?!\{)(?:[^{}])+\})+\})+\}/,
							lookbehind: true,
							inside: {
								'format-spec': {
									pattern: /(:)[^:(){}]+(?=\}$)/,
									lookbehind: true
								},
								'conversion-option': {
									pattern: /![sra](?=[:}]$)/,
									alias: 'punctuation'
								},
								rest: null
							}
						},
						'string': /[\s\S]+/
					}
				},
				'triple-quoted-string': {
					pattern: /(?:[rub]|rb|br)?("""|''')[\s\S]*?\1/i,
					greedy: true,
					alias: 'string'
				},
				'string': {
					pattern: /(?:[rub]|rb|br)?("|')(?:\\.|(?!\1)[^\\\r\n])*\1/i,
					greedy: true
				},
				'function': {
					pattern: /((?:^|\s)def[ \t]+)[a-zA-Z_]\w*(?=\s*\()/g,
					lookbehind: true
				},
				'class-name': {
					pattern: /(\bclass\s+)\w+/i,
					lookbehind: true
				},
				'decorator': {
					pattern: /(^[\t ]*)@\w+(?:\.\w+)*/im,
					lookbehind: true,
					alias: ['annotation', 'punctuation'],
					inside: {
						'punctuation': /\./
					}
				},
				'keyword': /\b(?:and|as|assert|async|await|break|class|continue|def|del|elif|else|except|exec|finally|for|from|global|if|import|in|is|lambda|nonlocal|not|or|pass|print|raise|return|try|while|with|yield)\b/,
				'builtin': /\b(?:__import__|abs|all|any|apply|ascii|basestring|bin|bool|buffer|bytearray|bytes|callable|chr|classmethod|cmp|coerce|compile|complex|delattr|dict|dir|divmod|enumerate|eval|execfile|file|filter|float|format|frozenset|getattr|globals|hasattr|hash|help|hex|id|input|int|intern|isinstance|issubclass|iter|len|list|locals|long|map|max|memoryview|min|next|object|oct|open|ord|pow|property|range|raw_input|reduce|reload|repr|reversed|round|set|setattr|slice|sorted|staticmethod|str|sum|super|tuple|type|unichr|unicode|vars|xrange|zip)\b/,
				'boolean': /\b(?:True|False|None)\b/,
				'number': /\b0(?:b(?:_?[01])+|o(?:_?[0-7])+|x(?:_?[a-f0-9])+)\b|(?:\b\d+(?:_\d+)*(?:\.(?:\d+(?:_\d+)*)?)?|\B\.\d+(?:_\d+)*)(?:e[+-]?\d+(?:_\d+)*)?j?\b/i,
				'operator': /[-+%=]=?|!=|\*\*?=?|\/\/?=?|<[<=>]?|>[=>]?|[&|^~]/,
				'punctuation': /[{}[\];(),.:]/
			}
		},

		hooks: {
			all: {},
			add: function (name, callback) {
				var hooks = _.hooks.all;
				hooks[name] = hooks[name] || [];
				hooks[name].push(callback);
			},
			run: function (name, env) {
				var callbacks = _.hooks.all[name];
				if (!callbacks || !callbacks.length) {
					return;
				}
				for (var i = 0, callback; callback = callbacks[i++];) {
					callback(env);
				}
			}
		},

		Token: Token
	};

	_self.Prism = _;

	function Token(type, content, alias, matchedStr) {
		this.type = type;
		this.content = content;
		this.alias = alias;
		this.length = (matchedStr || '').length | 0;
	}

	Token.stringify = function stringify(o, language) {
		if (typeof o == 'string') {
			return o;
		}

		if (Array.isArray(o)) {
			var s = '';
			o.forEach(function (e) {
				s += stringify(e, language);
			});
			return s;
		}

		var env = {
			type: o.type,
			content: stringify(o.content, language),
			tag: 'span',
			classes: ['token', o.type],
			attributes: {},
			language: language
		};

		var aliases = o.alias;
		if (aliases) {
			if (Array.isArray(aliases)) {
				Array.prototype.push.apply(env.classes, aliases);
			} else {
				env.classes.push(aliases);
			}
		}

		_.hooks.run('wrap', env);

		var attributes = '';
		for (var name in env.attributes) {
			attributes += ' ' + name + '="' + (env.attributes[name] || '').replace(/"/g, '&quot;') + '"';
		}

		return '<' + env.tag + ' class="' + env.classes.join(' ') + '"' + attributes + '>' + env.content + '</' + env.tag + '>';
	};

	return _;
})(_self);

if (typeof module !== 'undefined' && module.exports) {
	module.exports = Prism;
}

/* Plugin: Line Numbers */
(function() {
	if (typeof Prism === 'undefined' || typeof document === 'undefined') {
		return;
	}

	var PLUGIN_NAME = 'line-numbers';
	var NEW_LINE_EXP = /\n(?!$)/g;

	var isLineNumbersLoaded = function(element) {
		return element.classList.contains(PLUGIN_NAME);
	};

	var highlightLines = function(pre) {
		if (!pre || !/pre/i.test(pre.nodeName)) {
			return;
		}

		if (isLineNumbersLoaded(pre)) {
			return;
		}

		pre.classList.add(PLUGIN_NAME);

		var code = pre.querySelector('code');
		var lines = (code.textContent || '').split(NEW_LINE_EXP);
		var lineNumbersWrapper = document.createElement('span');
		lineNumbersWrapper.setAttribute('aria-hidden', 'true');
		lineNumbersWrapper.className = 'line-numbers-rows';

		for (var i = 0; i < lines.length; i++) {
			var line = document.createElement('span');
			lineNumbersWrapper.appendChild(line);
		}

		if (pre.hasAttribute('data-start')) {
			pre.style.counterReset = 'linenumber ' + (parseInt(pre.getAttribute('data-start'), 10) - 1);
		}

		pre.appendChild(lineNumbersWrapper);
	};

	Prism.hooks.add('complete', function(env) {
		var pre = env.element.parentElement;
		highlightLines(pre);
	});

	// Initialize on page load
	if (document.readyState === 'loading') {
		document.addEventListener('DOMContentLoaded', function() {
			document.querySelectorAll('pre').forEach(highlightLines);
		});
	} else {
		document.querySelectorAll('pre').forEach(highlightLines);
	}
})();

/* Custom navigation and reading time calculator */
document.addEventListener('DOMContentLoaded', function() {
	// Calculate reading time
	const content = document.querySelector('body').innerText;
	const wordsPerMinute = 200;
	const words = content.trim().split(/\s+/).length;
	const readingTime = Math.ceil(words / wordsPerMinute);
	
	// Insert reading time if container exists
	const readingTimeElement = document.querySelector('.reading-time');
	if (readingTimeElement) {
		readingTimeElement.textContent = `${readingTime} min read`;
	}
	
	// Progress indicator
	const progressBar = document.querySelector('.progress-bar');
	if (progressBar) {
		window.addEventListener('scroll', function() {
			const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
			const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
			const scrolled = (winScroll / height) * 100;
			progressBar.style.width = scrolled + '%';
		});
	}
	
	// Apply syntax highlighting to all code blocks
	document.querySelectorAll('pre code').forEach((block) => {
		// Add Python class if not present
		if (!block.className.includes('language-')) {
			block.className = 'language-python';
		}
		
		// Add line numbers to longer code blocks
		if (block.textContent.split('\n').length > 5) {
			block.parentElement.classList.add('line-numbers');
		}
		
		// Apply Prism highlighting if available
		if (typeof Prism !== 'undefined') {
			Prism.highlightElement(block);
		}
	});
	
	// Add mobile diagram notes after canvas elements
	document.querySelectorAll('canvas').forEach((canvas) => {
		const note = document.createElement('div');
		note.className = 'mobile-diagram-note';
		note.textContent = '📱 Diagram optimized for desktop viewing';
		canvas.parentNode.insertBefore(note, canvas.nextSibling);
	});
	
	// Add ARIA labels to interactive elements
	document.querySelectorAll('a').forEach((link) => {
		if (!link.getAttribute('aria-label') && link.textContent) {
			link.setAttribute('aria-label', link.textContent.trim());
		}
	});
	
	// Keyboard navigation for lesson navigation
	const prevLink = document.querySelector('.prev-lesson');
	const nextLink = document.querySelector('.next-lesson');
	
	document.addEventListener('keydown', function(e) {
		// Alt + Left Arrow for previous lesson
		if (e.altKey && e.key === 'ArrowLeft' && prevLink) {
			prevLink.click();
		}
		// Alt + Right Arrow for next lesson
		if (e.altKey && e.key === 'ArrowRight' && nextLink) {
			nextLink.click();
		}
	});
});