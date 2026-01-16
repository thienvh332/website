To use this module, add the ``content_only`` parameter to any portal URL:

* ``/my/orders/123?content_only=1`` - Hide header and footer
* ``/my/orders/123?content_only=0`` - Show header and footer (default)

**Supported truthy values:** ``1``, ``true``

**Supported falsy values:** ``0``, ``false``

Toggle Button
~~~~~~~~~~~~~

A small toggle button is available on the left side of the screen (vertically centered).
Click it to quickly switch between content-only mode and normal mode.

* **Purple button**: Content-only mode is OFF (header/footer visible)
* **Green button**: Content-only mode is ON (header/footer hidden)

Session Persistence
~~~~~~~~~~~~~~~~~~~

When you visit a page with ``content_only=1``, the preference is stored in
your session. Subsequent page visits will automatically include the
``content_only`` parameter until you explicitly disable it with
``content_only=0`` or click the toggle button.
