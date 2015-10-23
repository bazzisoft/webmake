
var Component = React.createClass(
{
    render: function()
    {
        console.log('foobars');
        return (
          <div>
            <h3>React.js Component</h3>
            <Subcomponent name="foo"/>
          </div>
        );
    },
});
