tenso.libs.logging
==================

.. py:module:: tenso.libs.logging

.. autoapi-nested-parse::

   Interface to logging package.



Classes
-------

.. autoapisummary::

   tenso.libs.logging.Logger


Module Contents
---------------

.. py:class:: Logger(filename: Optional[str] = None, level: Literal['debug', 'info', 'warning', 'error', 'critical'] = 'info', stream_fmt: Optional[str] = None, file_fmt: str = '%(message)s')

   Bases: :py:obj:`object`


   .. py:attribute:: levels


   .. py:attribute:: _logger


   .. py:method:: info(message: str)

      Log an info message.



   .. py:method:: debug(message: str)

      Log a debug message.



   .. py:method:: warning(message: str)

      Log a warning message.



   .. py:method:: error(message: str)

      Log an error message.



   .. py:method:: critical(message: str)

      Log a critical message.



   .. py:method:: __del__()

      Close the file handler when the logger is deleted.



