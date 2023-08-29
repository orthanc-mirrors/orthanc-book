import orthanc
import platform

def ExecutePython(output, uri, **request):
    s = 'Python version: %s' % platform.python_version()
    output.AnswerBuffer(s, 'text/plain')

orthanc.RegisterRestCallback('/execute-python', ExecutePython)

orthanc.ExtendOrthancExplorer('''
$('#lookup').live('pagebeforeshow', function() {
  $('#sample-python-button').remove();

  var b = $('<a>')
      .attr('id', 'sample-python-button')
      .attr('data-role', 'button')
      .attr('href', '#')
      .attr('data-icon', 'forward')
      .attr('data-theme', 'a')
      .text('Execute sample Python plugin')
      .button()
      .click(function(e) {
        $.get('../execute-python', function(answer) {
          alert(answer);
        });
      });

  b.insertAfter($('#lookup-result'));
});
''')
