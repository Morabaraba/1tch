'use strict';
/* global $ _ app Backbone */
(function(root) {
	$(main) // on ready call main
	function main() {
		$.get('pages/extracted.csv', function( data ) {
			setupLayout(data);
		})
	}
	function setupLayout(title) {
		
		var config0 = {
			content: [{
				type: 'row',
				content: [{
					title: title,
					type: 'component',
					componentName: 'snapgrid',
					componentState: {
						url: 'pages/pkgs.csv',
						fetchType: 'GET',
						/*counterChart: {
							contentItemId: 'chart',
							columnId: 'price'
						}*/
					}
				}, ]
			}]
		}

		app.state.layout.layoutCount = 1
		app.dispatcher.trigger('js:GoldenLayout.Create', { config: config0 })
	

		app.dispatcher.trigger('js:GoldenLayout.registerComponent', { component: app.component.ExampleComponent })
		app.dispatcher.trigger('js:GoldenLayout.registerComponent', { name: 'element', component: app.component.ElementComponent })
		app.dispatcher.trigger('js:GoldenLayout.registerComponent', { name: 'chart', component: app.component.ChartComponent })
		app.dispatcher.trigger('js:GoldenLayout.registerComponent', { name: 'snapgrid', component: app.component.SnapGridComponent })

		app.dispatcher.trigger('js:GoldenLayout.init')

		app.dispatcher.trigger('js:hideMenu', true)

		app.util.setupDocumentKeypressEvents() // should we do this with a trigger?
	}
})(window)